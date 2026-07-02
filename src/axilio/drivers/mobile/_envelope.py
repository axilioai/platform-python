"""DCP wire constants (mirrors commons/go/types/backend/realtime/dcp.go).

The Device Control Protocol is literal CDP: the driver's helper methods
emit these "Domain.method" names and both transports send them verbatim —
RemoteTransport as WebSocket messages, SandboxTransport as newline-delimited
JSON on the in-VM daemon's Unix socket. Same frames either way:
``{"id", "method", "params"}`` out, ``{"id", "result"|"error"}`` back.
"""

from __future__ import annotations

METHOD_INPUT_TAP = "Input.tap"
METHOD_INPUT_LONG_PRESS = "Input.longPress"
METHOD_INPUT_SWIPE = "Input.swipe"
METHOD_INPUT_TYPE_TEXT = "Input.typeText"
METHOD_INPUT_KEY_PRESS = "Input.keyPress"
METHOD_SCREEN_SCREENSHOT = "Screen.screenshot"
METHOD_SCREEN_OBSERVE = "Screen.observe"
METHOD_SCREEN_FIND = "Screen.find"

# DCP error kinds (the `data.kind` on a CDP error frame). PascalCase to
# mirror the Go side; mapped to the exception taxonomy in
# _errors.from_dcp_error.
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
