"""Exception hierarchy — daemon wire error codes map one-to-one to exceptions."""

from __future__ import annotations

from . import _envelope


class AxilioError(Exception):
    """Base for every error raised by this SDK."""

    code: str = _envelope.CODE_INTERNAL
    retryable: bool = False

    def __init__(self, message: str = "", *, retryable: bool | None = None) -> None:
        super().__init__(message)
        self.message = message
        if retryable is not None:
            self.retryable = retryable


class UnknownOpError(AxilioError):
    """Daemon doesn't recognise the op (SDK/daemon version skew)."""

    code = _envelope.CODE_UNKNOWN_OP


class InvalidArgsError(AxilioError):
    """Args failed validation."""

    code = _envelope.CODE_INVALID_ARGS


class NoAllocationError(AxilioError):
    """Daemon has no active allocation."""

    code = _envelope.CODE_NO_ALLOCATION


class NotConnectedError(AxilioError):
    """Daemon couldn't reach the on-device agent."""

    code = _envelope.CODE_NOT_CONNECTED


class DeviceOfflineError(AxilioError):
    """Device is transiently unavailable. Retryable."""

    code = _envelope.CODE_DEVICE_OFFLINE
    retryable = True


class UnauthorizedError(AxilioError):
    """Session token rejected by the on-device agent."""

    code = _envelope.CODE_UNAUTHORIZED


class InternalError(AxilioError):
    """Unclassified failure on the daemon side."""

    code = _envelope.CODE_INTERNAL


class CanceledError(AxilioError):
    """Operation canceled (deadline exceeded or context canceled)."""

    code = _envelope.CODE_CANCELED


class ConnectionError(AxilioError):  # noqa: A001 — shadow of builtin is intentional
    """SDK couldn't open the Unix socket."""


class ElementNotFoundError(AxilioError):
    """A selector found nothing."""

    code = "element_not_found"


class TimeoutError(AxilioError):  # noqa: A001 — shadow of builtin is intentional
    """A call or a `wait_*` poll loop exceeded its deadline."""

    code = "timeout"
    retryable = True


_CODE_TO_EXCEPTION: dict[str, type[AxilioError]] = {
    _envelope.CODE_UNKNOWN_OP: UnknownOpError,
    _envelope.CODE_INVALID_ARGS: InvalidArgsError,
    _envelope.CODE_NO_ALLOCATION: NoAllocationError,
    _envelope.CODE_NOT_CONNECTED: NotConnectedError,
    _envelope.CODE_DEVICE_OFFLINE: DeviceOfflineError,
    _envelope.CODE_UNAUTHORIZED: UnauthorizedError,
    _envelope.CODE_INTERNAL: InternalError,
    _envelope.CODE_CANCELED: CanceledError,
}


def from_wire(err: _envelope.WireError) -> AxilioError:
    """Map a wire-level error to the matching exception class."""
    cls = _CODE_TO_EXCEPTION.get(err.code, InternalError)
    return cls(err.message, retryable=err.retryable)
