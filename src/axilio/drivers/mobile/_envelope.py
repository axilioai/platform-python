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
