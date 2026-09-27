"""Exception hierarchy — DCP error kinds map one-to-one to exceptions."""

from __future__ import annotations

import builtins
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
    4409). Terminal for this transport; surfaced, never auto-retried (a
    retry loop against a held lease is the one-controller model's failure
    mode)."""

    code = "control_held"


class TimeoutError(AxilioError):  # noqa: A001 — shadow of builtin is intentional
    """A call or a `wait_*` poll loop exceeded its deadline."""

    code = "timeout"
    retryable = True


class StrategyUnavailableError(AxilioError):
    """The requested (or auto-picked) resolver needs a capability this
    session doesn't have; e.g. `role`/`id`-based selectors need the
    accessibility tree, which today's phones don't expose. Not retryable:
    the same locator or strategy fails identically on retry."""

    code = "strategy_unavailable"


class ActionTimeoutError(AxilioError, builtins.TimeoutError):
    """A Locator action's auto-wait exceeded its `timeoutMs` budget without
    the target becoming actionable. Not retryable: the target won't
    resolve without something on screen changing. Also catchable as the
    builtin `TimeoutError`, since that's what this is."""

    code = "action_timeout"


# DCP error `data.kind` → exception. The error frame carries a
# machine-readable PascalCase kind; each maps 1:1 onto the taxonomy above.
# Timeout stays mapped even though the driver usually raises it locally; a
# remote executor may surface it too.
_KIND_TO_EXCEPTION: dict[str, type[AxilioError]] = {
    _envelope.KIND_UNKNOWN_OP: UnknownOpError,
    _envelope.KIND_INVALID_ARGS: InvalidArgsError,
    _envelope.KIND_NO_ALLOCATION: NoAllocationError,
    _envelope.KIND_NOT_CONNECTED: NotConnectedError,
    _envelope.KIND_DEVICE_OFFLINE: DeviceOfflineError,
    _envelope.KIND_TIMEOUT: TimeoutError,
    _envelope.KIND_UNAUTHORIZED: UnauthorizedError,
    _envelope.KIND_INTERNAL: InternalError,
    _envelope.KIND_CANCELED: CanceledError,
    _envelope.KIND_ACTION_TIMEOUT: ActionTimeoutError,
    _envelope.KIND_STRATEGY_UNAVAILABLE: StrategyUnavailableError,
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
