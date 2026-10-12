"""What scripts/fix_generated_runtime.py changes in Fern's generated runtime,
checked through the generated client the way callers use it."""

from __future__ import annotations

import asyncio
import datetime as dt
import typing

import httpx
import pytest

from axilio.client import AsyncAxilioApi, AxilioApi
from axilio.core.api_error import ApiError
from axilio.types.api_key_create_response import ApiKeyCreateResponse
from axilio.types.phone_allocate_response import PhoneAllocateResponse
from axilio.types.webhook_endpoint_create_response import WebhookEndpointCreateResponse
from axilio.types.webhook_rotate_secret_response import WebhookRotateSecretResponse

CREATED = {
    "id": "we_1",
    "type": "webhook",
    "created_at": "2026-10-12T09:00:00Z",
    "secret": "whsec_test",
    "endpoints": [],
}


def _api(*statuses: int) -> tuple[AxilioApi, list[httpx.Request]]:
    """A client whose server answers each request with the next status in
    statuses (repeating the last), recording the requests it saw."""
    seen: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        seen.append(request)
        status = statuses[min(len(seen), len(statuses)) - 1]
        body = CREATED if status < 300 else {"detail": "error"}
        return httpx.Response(status, json=body, headers={"Retry-After-Ms": "1"})

    http = httpx.Client(transport=httpx.MockTransport(handler))
    return AxilioApi(base_url="https://api.test", api_key="ax_test", httpx_client=http), seen


def _handler_failing_once(
    error: type[httpx.TransportError],
) -> tuple[typing.Callable[[httpx.Request], httpx.Response], list[httpx.Request]]:
    """A server whose connection fails with error on the first request and that
    answers every later one, recording the requests it saw."""
    seen: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        seen.append(request)
        if len(seen) == 1:
            raise error("connection lost", request=request)
        return httpx.Response(201, json=CREATED)

    return handler, seen


def _api_failing_once(error: type[httpx.TransportError]) -> tuple[AxilioApi, list[httpx.Request]]:
    handler, seen = _handler_failing_once(error)
    http = httpx.Client(transport=httpx.MockTransport(handler))
    return AxilioApi(base_url="https://api.test", api_key="ax_test", httpx_client=http), seen


def test_post_is_not_resent_after_server_error() -> None:
    api, seen = _api(500, 201)
    with pytest.raises(ApiError):
        api.webhooks.create_endpoint(url="https://example.com/hook")
    assert len(seen) == 1, "a POST that may have taken effect must not be sent twice"


def test_post_is_resent_after_too_many_requests() -> None:
    api, seen = _api(429, 201)
    api.webhooks.create_endpoint(url="https://example.com/hook")
    assert [r.method for r in seen] == ["POST", "POST"]


def test_get_is_resent_after_server_error() -> None:
    api, seen = _api(500, 200)
    api.webhooks.list_endpoints()
    assert len(seen) == 2


def test_post_is_not_resent_after_a_dropped_connection() -> None:
    api, seen = _api_failing_once(httpx.RemoteProtocolError)
    with pytest.raises(httpx.RemoteProtocolError):
        api.webhooks.create_endpoint(url="https://example.com/hook")
    assert len(seen) == 1, "a POST whose connection dropped may have taken effect"


def test_async_post_is_not_resent_after_a_dropped_connection() -> None:
    handler, seen = _handler_failing_once(httpx.RemoteProtocolError)

    async def create() -> None:
        async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as http:
            api = AsyncAxilioApi(base_url="https://api.test", api_key="ax_test", httpx_client=http)
            await api.webhooks.create_endpoint(url="https://example.com/hook")

    with pytest.raises(httpx.RemoteProtocolError):
        asyncio.run(create())
    assert len(seen) == 1


def test_post_is_resent_when_the_connection_never_opened() -> None:
    api, seen = _api_failing_once(httpx.ConnectError)
    api.webhooks.create_endpoint(url="https://example.com/hook")
    assert [r.method for r in seen] == ["POST", "POST"]


def test_get_is_resent_after_a_dropped_connection() -> None:
    api, seen = _api_failing_once(httpx.RemoteProtocolError)
    api.webhooks.list_endpoints()
    assert len(seen) == 2


@pytest.mark.parametrize(
    ("model", "field", "secret"),
    [
        (WebhookEndpointCreateResponse, "secret", "whsec_create"),
        (WebhookRotateSecretResponse, "secret", "whsec_rotate"),
        (ApiKeyCreateResponse, "key_value", "ax_live_key"),
    ],
)
def test_repr_hides_secrets(model: type, field: str, secret: str) -> None:
    value = model(
        id="we_1",
        type="webhook",
        name="ci",
        created_at="2026-10-12T09:00:00Z",
        **{field: secret},
    )
    assert secret not in repr(value)
    assert secret not in str(value)
    assert "[redacted]" in repr(value)
    assert getattr(value, field) == secret
    assert value.model_dump()[field] == secret


def test_repr_shows_an_absent_secret_as_none() -> None:
    created_at = dt.datetime(2026, 10, 12, 9, tzinfo=dt.timezone.utc)
    value = WebhookEndpointCreateResponse(id="we_1", type="webhook", created_at=created_at)
    assert "secret=None" in repr(value)


@pytest.mark.parametrize("field", ["live_view_url", "control_url", "telemetry_url"])
def test_repr_hides_session_urls(field: str) -> None:
    url = "wss://connect.test/ws?token=tok_session"
    value = PhoneAllocateResponse(
        phone_id="ph_1",
        session_id="ss_1",
        workflow_started_at=dt.datetime(2026, 10, 12, 9, tzinfo=dt.timezone.utc),
        **{field: url},
    )
    assert "tok_session" not in repr(value)
    assert "tok_session" not in str(value)
    assert getattr(value, field) == url
