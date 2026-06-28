"""Wire envelope shared with the Go-side daemon (mirrors commons/go/types/control)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

OP_TAP = "tap"
OP_SWIPE = "swipe"
OP_KEY_PRESS = "key_press"
OP_TYPE = "type"
OP_SCREENSHOT = "screenshot"
OP_OBSERVE = "observe"
OP_SEMANTIC_FIND = "semantic_find"
OP_LONG_PRESS = "long_press"


CODE_UNKNOWN_OP = "unknown_op"
CODE_INVALID_ARGS = "invalid_args"
CODE_NO_ALLOCATION = "no_allocation"
CODE_NOT_CONNECTED = "not_connected"
CODE_DEVICE_OFFLINE = "device_offline"
CODE_UNAUTHORIZED = "unauthorized"
CODE_INTERNAL = "internal"
CODE_CANCELED = "canceled"


# --- DCP (control WebSocket) wire constants ---------------------------
# The Device Control Protocol is literal CDP: the driver's helper methods
# emit these "Domain.method" names, RemoteTransport sends them verbatim on
# the WebSocket, and the on-device agent executes them. SandboxTransport
# bridges them to the legacy daemon OP_* above (the daemon converges to
# DCP separately), so the two transports share one driver-facing protocol.

METHOD_INPUT_TAP = "Input.tap"
METHOD_INPUT_LONG_PRESS = "Input.longPress"
METHOD_INPUT_SWIPE = "Input.swipe"
METHOD_INPUT_TYPE_TEXT = "Input.typeText"
METHOD_INPUT_KEY_PRESS = "Input.keyPress"
METHOD_SCREEN_SCREENSHOT = "Screen.screenshot"
METHOD_SCREEN_OBSERVE = "Screen.observe"
METHOD_SCREEN_FIND = "Screen.find"

# DCP method → in-VM daemon op, for SandboxTransport's bridge. The params
# and result shapes are identical across both transports, so only the
# method name is translated; this map disappears when the daemon speaks
# DCP natively.
METHOD_TO_OP = {
    METHOD_INPUT_TAP: OP_TAP,
    METHOD_INPUT_LONG_PRESS: OP_LONG_PRESS,
    METHOD_INPUT_SWIPE: OP_SWIPE,
    METHOD_INPUT_TYPE_TEXT: OP_TYPE,
    METHOD_INPUT_KEY_PRESS: OP_KEY_PRESS,
    METHOD_SCREEN_SCREENSHOT: OP_SCREENSHOT,
    METHOD_SCREEN_OBSERVE: OP_OBSERVE,
    METHOD_SCREEN_FIND: OP_SEMANTIC_FIND,
}

# DCP error kinds (the `data.kind` on a CDP error frame). PascalCase to
# mirror the Go side (commons/go/types/backend/realtime/dcp.go); mapped to
# the exception taxonomy in _errors.from_dcp_error.
KIND_UNKNOWN_OP = "UnknownOp"
KIND_INVALID_ARGS = "InvalidArgs"
KIND_NO_ALLOCATION = "NoAllocation"
KIND_NOT_CONNECTED = "NotConnected"
KIND_DEVICE_OFFLINE = "DeviceOffline"
KIND_ELEMENT_NOT_FOUND = "ElementNotFound"
KIND_TIMEOUT = "Timeout"
KIND_UNAUTHORIZED = "Unauthorized"
KIND_INTERNAL = "Internal"
KIND_CANCELED = "Canceled"


@dataclass
class Command:
    """A single client→daemon request frame."""

    id: str
    op: str
    args: dict[str, Any] | None = None

    def to_wire(self) -> dict[str, Any]:
        """Serialise to the JSON shape the daemon expects."""
        out: dict[str, Any] = {"id": self.id, "op": self.op}
        if self.args is not None:
            out["args"] = self.args
        return out


@dataclass
class WireError:
    """Error payload on a failed Response."""

    code: str
    message: str
    retryable: bool = False

    @classmethod
    def from_wire(cls, data: dict[str, Any]) -> WireError:
        return cls(
            code=data.get("code", CODE_INTERNAL),
            message=data.get("message", ""),
            retryable=data.get("retryable", False),
        )


@dataclass
class Response:
    """A single daemon→client reply frame, paired with a Command by id."""

    id: str
    ok: bool
    result: dict[str, Any] | None = None
    error: WireError | None = None

    @classmethod
    def from_wire(cls, data: dict[str, Any]) -> Response:
        err = data.get("error")
        return cls(
            id=data.get("id", ""),
            ok=data.get("ok", False),
            result=data.get("result"),
            error=WireError.from_wire(err) if err else None,
        )
