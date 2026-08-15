"""DCP wire constants (mirrors commons/go/types/backend/realtime/dcp.go).

The Device Control Protocol is literal CDP: the driver's helper methods
emit these "Domain.method" names and both transports send them verbatim —
RemoteTransport as WebSocket messages, SandboxTransport as newline-delimited
JSON on the in-VM daemon's Unix socket. Same frames either way:
``{"id", "method", "params"}`` out, ``{"id", "result"|"error"}`` back.
"""

from __future__ import annotations

# DCP v1 (AXI-1785) groups the input verbs by device-class capability profile:
# the touch verbs are in the Touch domain, the text/key verbs in Keyboard,
# replacing the old flat Input domain. Screen stays the universal perception
# domain. Requires a v1 executor; released in lockstep with it (AXI-1788).
METHOD_TOUCH_TAP = "Touch.tap"
METHOD_TOUCH_LONG_PRESS = "Touch.longPress"
METHOD_TOUCH_SWIPE = "Touch.swipe"
METHOD_KEYBOARD_TYPE_TEXT = "Keyboard.typeText"
METHOD_KEYBOARD_KEY_PRESS = "Keyboard.keyPress"
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
