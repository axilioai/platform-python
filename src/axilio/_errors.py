"""Exception hierarchy for the Axilio SDK.

AxilioError is the catch-all base; specific subclasses for the common
cases let user code catch the right thing cleanly. Mirrors the HTTP
status codes the backend returns, plus a couple of SDK-specific
conditions (sandbox-mode write attempts, allocation mismatch).
"""

from __future__ import annotations


class AxilioError(Exception):
    """Base for every error raised by this SDK. Carries the HTTP status
    code (when relevant) and the raw response body for diagnostics."""

    status_code: int | None = None

    def __init__(
        self,
        message: str = "",
        *,
        status_code: int | None = None,
        body: str = "",
    ) -> None:
        super().__init__(message)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.body = body


class UnauthorizedError(AxilioError):
    """API key missing, malformed, or rejected by the backend (401)."""

    status_code = 401


class NotFoundError(AxilioError):
    """Requested resource doesn't exist or isn't visible to this caller (404)."""

    status_code = 404


class RateLimitError(AxilioError):
    """Backend rate-limited the caller (429). Retryable after a backoff."""

    status_code = 429


class ServerError(AxilioError):
    """Backend returned 5xx. Usually transient; safe to retry with backoff."""

    status_code = 500


class SandboxPermissionError(AxilioError):
    """Raised when sandbox-mode code attempts a write that's only
    permitted in local mode (e.g. cancelling a subscription, revoking
    API keys). The design doc spells out the read-only sandbox surface;
    this is its enforcement point."""


class AllocationMismatchError(AxilioError):
    """Raised when a sandbox script calls devices.allocate(...) with
    kwargs (platform, location, apps) that don't match what the VM was
    actually given. Surfaces local→sandbox migration issues clearly
    instead of silently ignoring the kwargs."""


_STATUS_TO_EXCEPTION: dict[int, type[AxilioError]] = {
    401: UnauthorizedError,
    404: NotFoundError,
    429: RateLimitError,
}


def from_response(status_code: int, body: str) -> AxilioError:
    """Map an HTTP response to the right exception class. 5xx all funnel
    into ServerError; specific 4xx codes get their own classes; anything
    else falls back to the base."""
    if 500 <= status_code < 600:
        return ServerError(
            f"backend returned {status_code}",
            status_code=status_code,
            body=body,
        )
    cls = _STATUS_TO_EXCEPTION.get(status_code, AxilioError)
    return cls(
        f"backend returned {status_code}",
        status_code=status_code,
        body=body,
    )
