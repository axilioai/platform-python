"""DCP wire constants — re-exported from the generated wire layer.

The Device Control Protocol is literal CDP: the driver's helper methods emit
these "Domain.method" names and both transports send them verbatim —
RemoteTransport as WebSocket messages, SandboxTransport as newline-delimited
JSON on the in-VM daemon's Unix socket. Same frames either way:
``{"id", "method", "params"}`` out, ``{"id", "result"|"error"}`` back.

The method names and error kinds below used to be hand-maintained to mirror the
Go server. They are now generated from the vendored DCP contract into
:mod:`._wire` (see ``scripts/generate_dcp_wire.py``); this module re-exports them
so call sites are unchanged while the source of truth is the contract.
"""

from __future__ import annotations

from ._wire import (
    KIND_CANCELED,
    KIND_DEVICE_OFFLINE,
    KIND_ELEMENT_NOT_FOUND,
    KIND_INTERNAL,
    KIND_INVALID_ARGS,
    KIND_NO_ALLOCATION,
    KIND_NOT_CONNECTED,
    KIND_TIMEOUT,
    KIND_UNAUTHORIZED,
    KIND_UNKNOWN_OP,
    METHOD_DEVICE_INFO,
    METHOD_KEYBOARD_KEY_PRESS,
    METHOD_KEYBOARD_TYPE_TEXT,
    METHOD_PROTOCOL_HANDSHAKE,
    METHOD_SCREEN_FIND,
    METHOD_SCREEN_OBSERVE,
    METHOD_SCREEN_SCREENSHOT,
    METHOD_TOUCH_LONG_PRESS,
    METHOD_TOUCH_SWIPE,
    METHOD_TOUCH_TAP,
)

__all__ = [
    "KIND_CANCELED",
    "KIND_DEVICE_OFFLINE",
    "KIND_ELEMENT_NOT_FOUND",
    "KIND_INTERNAL",
    "KIND_INVALID_ARGS",
    "KIND_NO_ALLOCATION",
    "KIND_NOT_CONNECTED",
    "KIND_TIMEOUT",
    "KIND_UNAUTHORIZED",
    "KIND_UNKNOWN_OP",
    "METHOD_DEVICE_INFO",
    "METHOD_KEYBOARD_KEY_PRESS",
    "METHOD_KEYBOARD_TYPE_TEXT",
    "METHOD_PROTOCOL_HANDSHAKE",
    "METHOD_SCREEN_FIND",
    "METHOD_SCREEN_OBSERVE",
    "METHOD_SCREEN_SCREENSHOT",
    "METHOD_TOUCH_LONG_PRESS",
    "METHOD_TOUCH_SWIPE",
    "METHOD_TOUCH_TAP",
]
