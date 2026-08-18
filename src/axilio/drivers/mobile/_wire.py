"""Generated DCP wire layer - DO NOT EDIT.

Regenerate with `python scripts/generate_dcp_wire.py`. The source of truth is
the DCP AsyncAPI contract vendored at contracts/dcp-asyncapi.yaml, which the
backend publishes on every production deploy. tests/test_dcp_wire_drift.py
asserts this file equals that contract, so the typed layer can never fall out
of step with the deployed protocol."""

from __future__ import annotations

from dataclasses import dataclass

PROTOCOL_VERSION = 1

# --- command methods (Domain.method wire names) ---
METHOD_DEVICE_INFO = "Device.info"
METHOD_KEYBOARD_KEY_PRESS = "Keyboard.keyPress"
METHOD_KEYBOARD_TYPE_TEXT = "Keyboard.typeText"
METHOD_PROTOCOL_HANDSHAKE = "Protocol.handshake"
METHOD_SCREEN_FIND = "Screen.find"
METHOD_SCREEN_OBSERVE = "Screen.observe"
METHOD_SCREEN_SCREENSHOT = "Screen.screenshot"
METHOD_TOUCH_LONG_PRESS = "Touch.longPress"
METHOD_TOUCH_SWIPE = "Touch.swipe"
METHOD_TOUCH_TAP = "Touch.tap"

# --- error kinds + their (code, retryable) specs ---
KIND_UNKNOWN_OP = "UnknownOp"
KIND_INVALID_ARGS = "InvalidArgs"
KIND_INTERNAL = "Internal"
KIND_NO_ALLOCATION = "NoAllocation"
KIND_NOT_CONNECTED = "NotConnected"
KIND_DEVICE_OFFLINE = "DeviceOffline"
KIND_ELEMENT_NOT_FOUND = "ElementNotFound"
KIND_TIMEOUT = "Timeout"
KIND_UNAUTHORIZED = "Unauthorized"
KIND_CANCELED = "Canceled"

ERROR_SPECS: dict[str, tuple[int, bool]] = {
    "UnknownOp": (-32601, False),
    "InvalidArgs": (-32602, False),
    "Internal": (-32603, False),
    "NoAllocation": (-32001, False),
    "NotConnected": (-32002, False),
    "DeviceOffline": (-32004, True),
    "ElementNotFound": (-32005, False),
    "Timeout": (-32006, True),
    "Unauthorized": (-32007, False),
    "Canceled": (-32008, False),
}

# --- params / result models (one per contract schema) ---

@dataclass
class HandshakeParams:
    client_version: str | None = None
    min_protocol: int | None = None


@dataclass
class TouchTapParams:
    x: int
    y: int


@dataclass
class TouchLongPressParams:
    x: int
    y: int
    duration_ms: int | None = None


@dataclass
class TouchSwipeParams:
    x1: int
    y1: int
    x2: int
    y2: int
    duration_ms: int | None = None


@dataclass
class KeyboardTypeTextParams:
    text: str


@dataclass
class KeyboardKeyPressParams:
    usage: int | None = None
    key: str | None = None


@dataclass
class ObserveParams:
    ocr_engine: str | None = None


@dataclass
class FindParams:
    query: str
    model: str | None = None
    ocr_engine: str | None = None


@dataclass
class ScreenshotResult:
    png_base64: str


@dataclass
class DeviceInfo:
    device_id: str
    platform: str
    form_factor: str
    input_modalities: list[str]
    screen_width: int
    screen_height: int
    model: str | None = None
    os_version: str | None = None


@dataclass
class Bbox:
    x: int
    y: int
    width: int
    height: int


@dataclass
class Data:
    kind: str | None = None
    retryable: bool | None = None


@dataclass
class DcpError:
    code: int
    message: str
    data: Data | None = None


@dataclass
class HandshakeResult:
    protocol_version: int
    device: DeviceInfo
    domains: list[str]
    capabilities: list[str]


@dataclass
class ObserveText:
    text: str | None = None
    bbox: Bbox | None = None
    confidence: float | None = None


@dataclass
class ObserveIcon:
    bbox: Bbox | None = None
    confidence: float | None = None


@dataclass
class FindFound:
    bbox: Bbox | None = None
    confidence: float | None = None
    text: str | None = None


@dataclass
class ObserveResult:
    texts: list[ObserveText]
    icons: list[ObserveIcon]
    hash: str
    width: int
    height: int
    captured_at: int


@dataclass
class FindResult:
    found: FindFound | None = None
    model_name: str | None = None
    model_cost_microdollars: int | None = None
