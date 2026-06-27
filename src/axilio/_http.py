"""Thin HTTP transport over httpx.

Owns the request loop: builds the URL, sets the Bearer auth header,
fires the request, retries transient failures, and maps non-2xx
responses to AxilioError subclasses. Resource modules call into this
for every wire call rather than touching httpx directly so auth,
retries, and error mapping stay in one place.

Retries cover 429 (rate limited), 5xx (transient backend errors), and
transport-level failures (connection refused/reset, timeouts) — all
transient by nature. Up to ``max_retries`` extra attempts are made with
exponential backoff plus jitter; a ``Retry-After`` header on the
response takes precedence over the computed backoff. 4xx other than 429
fail fast — retrying a bad request or a missing resource never helps.
"""

from __future__ import annotations

import random
import time
from email.utils import parsedate_to_datetime
from typing import Any

import httpx

from . import _errors

# Cap any single backoff sleep so a server-supplied Retry-After or a
# large retry count can't park a request for minutes.
_MAX_BACKOFF_SECONDS = 30.0


class HTTPClient:
    """Wraps an httpx.Client with the Axilio SDK conventions:

        - Authorization: Bearer <api_key> on every request.
        - JSON request/response by default.
        - Non-2xx → AxilioError subclass via _errors.from_response.
        - Configurable base_url + timeout.

    Construct once per Client; share across all resources.
    """

    def __init__(
        self,
        *,
        api_key: str,
        base_url: str,
        timeout: float = 30.0,
        max_retries: int = 3,
        retry_base_delay: float = 0.5,
    ) -> None:
        self._api_key = api_key
        self._base_url = base_url.rstrip("/")
        self._timeout = timeout
        # Retry config: max_retries is the number of *extra* attempts
        # after the first, so the total request count is bounded at
        # max_retries + 1. retry_base_delay seeds the exponential
        # backoff. Clamp to 0 so a negative value can't loop forever.
        self._max_retries = max(0, max_retries)
        self._retry_base_delay = max(0.0, retry_base_delay)
        self._client = httpx.Client(
            base_url=self._base_url,
            timeout=self._timeout,
            headers={
                "Authorization": f"Bearer {self._api_key}",
                "Content-Type": "application/json",
                "Accept": "application/json",
            },
        )

    def close(self) -> None:
        """Release the underlying connection pool."""
        self._client.close()

    def request(
        self,
        method: str,
        path: str,
        *,
        json: Any | None = None,
        params: dict[str, Any] | None = None,
    ) -> Any:
        """Fire a request, retrying transient failures. Returns the
        decoded JSON body on 2xx; raises an AxilioError subclass once
        HTTP retries are exhausted (or immediately for non-retryable
        codes), or the underlying httpx error for network failures.

        429, 5xx, and transport-level errors (connect/read/write
        timeouts, connection resets) are retried up to ``max_retries``
        times with exponential backoff; everything else fails fast."""
        for attempt in range(self._max_retries + 1):
            try:
                response = self._client.request(
                    method,
                    path,
                    json=json,
                    params=params,
                )
            except httpx.TransportError:
                # Connection refused, reset, or a timeout — transient by
                # nature. Retry while attempts remain; otherwise let the
                # original httpx error propagate.
                if attempt < self._max_retries:
                    time.sleep(self._backoff_delay(attempt))
                    continue
                raise
            if 200 <= response.status_code < 300:
                if response.content:
                    return response.json()
                return None
            # Retry on rate limits and transient backend errors, but
            # only while attempts remain. The final failure raises.
            if attempt < self._max_retries and _is_retryable(response.status_code):
                time.sleep(self._backoff(attempt, response))
                continue
            raise _errors.from_response(response.status_code, response.text)
        # Unreachable: the loop either returns or raises on its last
        # iteration. Present so type checkers see a total function.
        raise AssertionError("retry loop exited without returning")

    def _backoff(self, attempt: int, response: httpx.Response) -> float:
        """Seconds to sleep before the next attempt after an HTTP error.

        A server-supplied ``Retry-After`` wins when present; otherwise
        fall back to the jittered exponential backoff."""
        retry_after = _parse_retry_after(response.headers.get("Retry-After"))
        if retry_after is not None:
            return min(retry_after, _MAX_BACKOFF_SECONDS)
        return self._backoff_delay(attempt)

    def _backoff_delay(self, attempt: int) -> float:
        """Exponential backoff (base * 2**attempt) with full jitter to
        avoid synchronised retries, capped at ``_MAX_BACKOFF_SECONDS``.
        ``attempt`` is 0-indexed (0 for the first retry)."""
        ceiling = min(self._retry_base_delay * (2**attempt), _MAX_BACKOFF_SECONDS)
        return random.uniform(0, ceiling)

    def get(self, path: str, *, params: dict[str, Any] | None = None) -> Any:
        return self.request("GET", path, params=params)

    def post(self, path: str, *, json: Any | None = None) -> Any:
        return self.request("POST", path, json=json)

    def put(self, path: str, *, json: Any | None = None) -> Any:
        return self.request("PUT", path, json=json)

    def patch(self, path: str, *, json: Any | None = None) -> Any:
        return self.request("PATCH", path, json=json)

    def delete(self, path: str) -> Any:
        return self.request("DELETE", path)


def _is_retryable(status_code: int) -> bool:
    """429 (rate limited) and 5xx (transient backend) are safe to retry;
    other 4xx are caller errors that won't change on a replay."""
    return status_code == 429 or 500 <= status_code < 600


def _parse_retry_after(value: str | None) -> float | None:
    """Parse a ``Retry-After`` header into seconds. Supports both the
    delta-seconds form (``"5"``) and the HTTP-date form
    (``"Wed, 21 Oct 2015 07:28:00 GMT"``). Returns None when absent or
    unparseable so the caller falls back to computed backoff."""
    if value is None:
        return None
    value = value.strip()
    if not value:
        return None
    try:
        return max(0.0, float(value))
    except ValueError:
        pass
    try:
        retry_at = parsedate_to_datetime(value)
    except (TypeError, ValueError):
        return None
    if retry_at is None:
        return None
    delta = retry_at.timestamp() - time.time()
    return max(0.0, delta)
