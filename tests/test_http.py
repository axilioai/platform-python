"""Tests for the HTTP transport's retry behaviour.

Covers the 429/5xx retry loop in HTTPClient.request: which status
codes retry, that retries are bounded by max_retries, that the loop
gives up and raises the mapped error, that non-retryable codes fail
fast, and that a Retry-After header drives the backoff. time.sleep is
stubbed throughout so the suite never actually waits.
"""

from __future__ import annotations

import httpx
import pytest

from axilio import _errors, _http
from axilio._http import HTTPClient, _is_retryable, _parse_retry_after


@pytest.fixture
def sleeps(monkeypatch: pytest.MonkeyPatch) -> list[float]:
    """Capture every backoff sleep instead of waiting on the clock."""
    recorded: list[float] = []
    monkeypatch.setattr(_http.time, "sleep", recorded.append)
    return recorded


def _make_client(**kwargs: object) -> HTTPClient:
    params: dict[str, object] = {
        "api_key": "ax_test",
        "base_url": "https://api.example",
    }
    params.update(kwargs)
    return HTTPClient(**params)  # type: ignore[arg-type]


def test_retries_429_then_succeeds(httpx_mock, sleeps: list[float]) -> None:
    httpx_mock.add_response(status_code=429)
    httpx_mock.add_response(json={"ok": True})
    client = _make_client(max_retries=3)
    try:
        assert client.get("/v1/thing") == {"ok": True}
        assert len(httpx_mock.get_requests()) == 2
        assert len(sleeps) == 1
    finally:
        client.close()


def test_retries_500_then_succeeds(httpx_mock, sleeps: list[float]) -> None:
    httpx_mock.add_response(status_code=503)
    httpx_mock.add_response(status_code=500)
    httpx_mock.add_response(json={"ok": True})
    client = _make_client(max_retries=3)
    try:
        assert client.get("/v1/thing") == {"ok": True}
        assert len(httpx_mock.get_requests()) == 3
        assert len(sleeps) == 2
    finally:
        client.close()


def test_exhausts_retries_then_raises(httpx_mock, sleeps: list[float]) -> None:
    httpx_mock.add_response(status_code=500, is_reusable=True)
    client = _make_client(max_retries=2)
    try:
        with pytest.raises(_errors.ServerError):
            client.get("/v1/thing")
        # 1 initial attempt + 2 retries = 3 requests, 2 sleeps.
        assert len(httpx_mock.get_requests()) == 3
        assert len(sleeps) == 2
    finally:
        client.close()


def test_429_exhaustion_raises_rate_limit(httpx_mock, sleeps: list[float]) -> None:
    httpx_mock.add_response(status_code=429, is_reusable=True)
    client = _make_client(max_retries=1)
    try:
        with pytest.raises(_errors.RateLimitError):
            client.get("/v1/thing")
        assert len(httpx_mock.get_requests()) == 2
    finally:
        client.close()


@pytest.mark.parametrize("status_code", [400, 401, 404, 422])
def test_non_retryable_fails_fast(httpx_mock, sleeps: list[float], status_code: int) -> None:
    httpx_mock.add_response(status_code=status_code)
    client = _make_client(max_retries=3)
    try:
        with pytest.raises(_errors.AxilioError):
            client.get("/v1/thing")
        # No retry on 4xx other than 429 — single request, no sleep.
        assert len(httpx_mock.get_requests()) == 1
        assert sleeps == []
    finally:
        client.close()


def test_max_retries_zero_disables_retry(httpx_mock, sleeps: list[float]) -> None:
    httpx_mock.add_response(status_code=500)
    client = _make_client(max_retries=0)
    try:
        with pytest.raises(_errors.ServerError):
            client.get("/v1/thing")
        assert len(httpx_mock.get_requests()) == 1
        assert sleeps == []
    finally:
        client.close()


def test_retry_after_seconds_drives_backoff(httpx_mock, sleeps: list[float]) -> None:
    httpx_mock.add_response(status_code=429, headers={"Retry-After": "7"})
    httpx_mock.add_response(json={"ok": True})
    client = _make_client(max_retries=3, retry_base_delay=0.5)
    try:
        client.get("/v1/thing")
        assert sleeps == [7.0]
    finally:
        client.close()


def test_retry_after_is_capped(httpx_mock, sleeps: list[float]) -> None:
    httpx_mock.add_response(status_code=503, headers={"Retry-After": "9999"})
    httpx_mock.add_response(json={"ok": True})
    client = _make_client(max_retries=3)
    try:
        client.get("/v1/thing")
        assert sleeps == [_http._MAX_BACKOFF_SECONDS]
    finally:
        client.close()


def test_computed_backoff_is_bounded(httpx_mock, sleeps: list[float]) -> None:
    """Without a Retry-After header, jittered exponential backoff stays
    within [0, base * 2**attempt]."""
    httpx_mock.add_response(status_code=500)
    httpx_mock.add_response(status_code=500)
    httpx_mock.add_response(json={"ok": True})
    client = _make_client(max_retries=3, retry_base_delay=0.5)
    try:
        client.get("/v1/thing")
        assert len(sleeps) == 2
        assert 0 <= sleeps[0] <= 0.5  # base * 2**0
        assert 0 <= sleeps[1] <= 1.0  # base * 2**1
    finally:
        client.close()


def test_is_retryable() -> None:
    assert _is_retryable(429)
    assert _is_retryable(500)
    assert _is_retryable(503)
    assert _is_retryable(599)
    assert not _is_retryable(200)
    assert not _is_retryable(400)
    assert not _is_retryable(401)
    assert not _is_retryable(404)


def test_parse_retry_after_seconds() -> None:
    assert _parse_retry_after("5") == 5.0
    assert _parse_retry_after("  10 ") == 10.0
    assert _parse_retry_after("-3") == 0.0  # clamped, never negative


def test_parse_retry_after_absent_or_garbage() -> None:
    assert _parse_retry_after(None) is None
    assert _parse_retry_after("") is None
    assert _parse_retry_after("not-a-date") is None


def test_parse_retry_after_http_date() -> None:
    # A date far in the past resolves to 0 (clamped), proving the
    # HTTP-date branch parses rather than returning None.
    past = "Wed, 21 Oct 2015 07:28:00 GMT"
    assert _parse_retry_after(past) == 0.0


def test_retry_loop_propagates_non_5xx_4xx_codes(httpx_mock, sleeps: list[float]) -> None:
    """A 3xx that httpx surfaces as a response (redirects disabled by
    default on the client) is not retryable and maps to the base error."""
    httpx_mock.add_response(status_code=301)
    client = _make_client(max_retries=3)
    try:
        with pytest.raises(_errors.AxilioError):
            client.get("/v1/thing")
        assert len(httpx_mock.get_requests()) == 1
    finally:
        client.close()


def test_retries_transport_error_then_succeeds(httpx_mock, sleeps: list[float]) -> None:
    httpx_mock.add_exception(httpx.ConnectError("connection refused"))
    httpx_mock.add_response(json={"ok": True})
    client = _make_client(max_retries=3)
    try:
        assert client.get("/v1/thing") == {"ok": True}
        assert len(sleeps) == 1
    finally:
        client.close()


def test_retries_timeout_then_succeeds(httpx_mock, sleeps: list[float]) -> None:
    # ReadTimeout is an httpx.TransportError subclass — also transient.
    httpx_mock.add_exception(httpx.ReadTimeout("timed out"))
    httpx_mock.add_response(json={"ok": True})
    client = _make_client(max_retries=3)
    try:
        assert client.get("/v1/thing") == {"ok": True}
        assert len(sleeps) == 1
    finally:
        client.close()


def test_transport_error_exhaustion_reraises(httpx_mock, sleeps: list[float]) -> None:
    httpx_mock.add_exception(httpx.ConnectError("connection refused"), is_reusable=True)
    client = _make_client(max_retries=2)
    try:
        # The original httpx error propagates once retries are spent.
        with pytest.raises(httpx.ConnectError):
            client.get("/v1/thing")
        assert len(sleeps) == 2
    finally:
        client.close()


def test_post_body_resent_on_retry(httpx_mock, sleeps: list[float]) -> None:
    """The JSON body is re-sent on each retry attempt, not dropped."""
    httpx_mock.add_response(status_code=500)
    httpx_mock.add_response(json={"ok": True})
    client = _make_client(max_retries=2)
    try:
        client.post("/v1/thing", json={"name": "widget"})
        requests = httpx_mock.get_requests()
        assert len(requests) == 2
        for req in requests:
            assert req.read() == b'{"name":"widget"}'
    finally:
        client.close()
