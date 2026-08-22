"""Exception hierarchy — DCP error kinds map one-to-one to exceptions."""

from __future__ import annotations

from typing import Any

from . import _envelope


class AxilioError(Exception):
    """Base for every error raised by this SDK."""

    code: str = "internal"
    retryable: bool = False

    def __init__(self, message: str = "", *, retryable: bool | None = None) -> None:
        super().__init__(message)
        self.message = message
        if retryable is not None:
            self.retryable = retryable


class UnknownOpError(AxilioError):
    """Executor doesn't recognise the method (SDK/daemon version skew)."""

    code = "unknown_op"


class InvalidArgsError(AxilioError):
    """Params failed validation."""

    code = "invalid_args"


class NoAllocationError(AxilioError):
    """Daemon has no active allocation."""

    code = "no_allocation"


class NotConnectedError(AxilioError):
    """Executor couldn't reach the on-device agent."""

    code = "not_connected"


class DeviceOfflineError(AxilioError):
    """Device is transiently unavailable. Retryable."""

    code = "device_offline"
    retryable = True


class UnauthorizedError(AxilioError):
    """Session token rejected by the on-device agent."""

    code = "unauthorized"


class InternalError(AxilioError):
    """Unclassified failure on the executor side."""

    code = "internal"


class CanceledError(AxilioError):
    """Operation canceled (deadline exceeded or context canceled)."""

    code = "canceled"


class ConnectionError(AxilioError):  # noqa: A001 — shadow of builtin is intentional
    """The transport's connection failed and could not be re-established
    within its bounded reconnect budget. Retryable: the allocation may
    still be live, so a later call can succeed."""

    code = "connection"
    retryable = True


class SessionEndedError(AxilioError):
    """The session is over: the server closed the control socket with 1000
    ("session ended", or this connection was superseded by a newer one) or
    refused the reattach with HTTP 403 (allocation no longer active).
    Terminal; never retried."""

    code = "session_ended"


class ControlHeldError(AxilioError):
    """Another controller holds the session's control lease (close code
    4409). Terminal for this transport; surfaced, never auto-retried — a
    retry loop against a held lease is the one-controller model's failure
    mode."""

    code = "control_held"


class ElementNotFoundError(AxilioError):
    """A selector found nothing."""

    code = "element_not_found"


class TimeoutError(AxilioError):  # noqa: A001 — shadow of builtin is intentional
    """A call or a `wait_*` poll loop exceeded its deadline."""

    code = "timeout"
    retryable = True


# DCP error `data.kind` → exception. The error frame carries a
# machine-readable PascalCase kind; each maps 1:1 onto the taxonomy above.
# Timeout / ElementNotFound stay mapped even though the driver usually
# raises those locally — a remote executor may surface them too.
_KIND_TO_EXCEPTION: dict[str, type[AxilioError]] = {
    _envelope.KIND_UNKNOWN_OP: UnknownOpError,
    _envelope.KIND_INVALID_ARGS: InvalidArgsError,
    _envelope.KIND_NO_ALLOCATION: NoAllocationError,
    _envelope.KIND_NOT_CONNECTED: NotConnectedError,
    _envelope.KIND_DEVICE_OFFLINE: DeviceOfflineError,
    _envelope.KIND_ELEMENT_NOT_FOUND: ElementNotFoundError,
    _envelope.KIND_TIMEOUT: TimeoutError,
    _envelope.KIND_UNAUTHORIZED: UnauthorizedError,
    _envelope.KIND_INTERNAL: InternalError,
    _envelope.KIND_CANCELED: CanceledError,
}


def from_dcp_error(error: dict[str, Any]) -> AxilioError:
    """Map a DCP error frame's ``error`` object to the matching exception.

    Shape: ``{"code": int, "message": str, "data": {"kind": str,
    "retryable": bool}}``. The kind drives the class; an unknown kind
    degrades to InternalError.
    """
    data = error.get("data") or {}
    kind = data.get("kind", _envelope.KIND_INTERNAL)
    cls = _KIND_TO_EXCEPTION.get(kind, InternalError)
    retryable = data.get("retryable")
    return cls(error.get("message", ""), retryable=retryable)
