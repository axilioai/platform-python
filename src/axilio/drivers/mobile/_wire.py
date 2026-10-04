"""Generated DCP wire layer - DO NOT EDIT.

Regenerate with `python scripts/generate_dcp_wire.py`. The source of truth is
the DCP AsyncAPI contract vendored at contracts/dcp-asyncapi.yaml, which the
backend publishes on every production deploy. tests/test_dcp_wire_drift.py
asserts this file equals that contract, so the typed layer can never fall out
of step with the deployed protocol."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, TypeAlias

PROTOCOL_VERSION = 1

# --- command methods (Domain.method wire names) ---
METHOD_ACCESSIBILITY_DISABLE = "Accessibility.disable"
METHOD_ACCESSIBILITY_ENABLE = "Accessibility.enable"
METHOD_ACCESSIBILITY_GET_CHILD_AXNODES = "Accessibility.getChildAXNodes"
METHOD_ACCESSIBILITY_GET_FULL_AXTREE = "Accessibility.getFullAXTree"
METHOD_ACCESSIBILITY_GET_PARTIAL_AXTREE = "Accessibility.getPartialAXTree"
METHOD_ACCESSIBILITY_GET_STATE = "Accessibility.getState"
METHOD_ACCESSIBILITY_QUERY_AXTREE = "Accessibility.queryAXTree"
METHOD_DEVICE_INFO = "Device.info"
METHOD_KEYBOARD_KEY_PRESS = "Keyboard.keyPress"
METHOD_KEYBOARD_TYPE_TEXT = "Keyboard.typeText"
METHOD_LOCATOR_BOUNDING_BOX = "Locator.boundingBox"
METHOD_LOCATOR_COUNT = "Locator.count"
METHOD_LOCATOR_FILL = "Locator.fill"
METHOD_LOCATOR_PRESS = "Locator.press"
METHOD_LOCATOR_TAP = "Locator.tap"
METHOD_LOCATOR_TEXT = "Locator.text"
METHOD_LOCATOR_WAIT_FOR = "Locator.waitFor"
METHOD_PROTOCOL_HANDSHAKE = "Protocol.handshake"
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
KIND_TIMEOUT = "Timeout"
KIND_UNAUTHORIZED = "Unauthorized"
KIND_CANCELED = "Canceled"
KIND_ACTION_TIMEOUT = "ActionTimeout"
KIND_STRATEGY_UNAVAILABLE = "StrategyUnavailable"
KIND_TREE_UNAVAILABLE = "TreeUnavailable"
KIND_STALE_NODE = "StaleNode"

ERROR_SPECS: dict[str, tuple[int, bool]] = {
    "UnknownOp": (-32601, False),
    "InvalidArgs": (-32602, False),
    "Internal": (-32603, False),
    "NoAllocation": (-32001, False),
    "NotConnected": (-32002, False),
    "DeviceOffline": (-32004, True),
    "Timeout": (-32006, True),
    "Unauthorized": (-32007, False),
    "Canceled": (-32008, False),
    "ActionTimeout": (-32009, False),
    "StrategyUnavailable": (-32010, False),
    "TreeUnavailable": (-32011, False),
    "StaleNode": (-32012, False),
}

# --- params / result models (one per contract schema) ---


@dataclass
class CursorParams:
    cursor: str


@dataclass
class ResyncRequiredParams:
    requested: str
    oldest: str | None = None


@dataclass
class HandshakeParams:
    client_version: str | None = None
    min_protocol: int | None = None


class Key(Enum):
    enter = "enter"
    capslock = "capslock"


IdempotencyKey: TypeAlias = str


@dataclass
class ObserveParams:
    ocr_engine: str | None = None


@dataclass
class AndroidLocator:
    className: str | None = None
    packageName: str | None = None


class LocatorStrategy(Enum):
    auto = "auto"
    vision = "vision"
    accessibility = "accessibility"


LocatorTimeoutMs: TypeAlias = int


LocatorOcrEngine: TypeAlias = str


LocatorModel: TypeAlias = str


class ResolvedBy(Enum):
    a11y = "a11y"
    ocr = "ocr"
    vlm = "vlm"


class State(Enum):
    visible = "visible"
    hidden = "hidden"
    enabled = "enabled"


@dataclass
class AccessibilityToggleParams:
    idempotencyKey: IdempotencyKey | None = None


@dataclass
class GetFullAXTreeParams:
    depth: int | None = None
    windowId: str | None = None
    interestingOnly: bool | None = True


@dataclass
class GetPartialAXTreeParams:
    nodeId: str
    fetchRelatives: bool | None = True


@dataclass
class GetChildAXNodesParams:
    id: str


@dataclass
class ScreenshotResult:
    png_base64: str


@dataclass
class LocatorCountResult:
    count: int
    resolvedBy: ResolvedBy
    tookMs: int
    modelName: str | None = None


@dataclass
class AccessibilityState:
    enabled: bool
    toggleable: bool


@dataclass
class AXValue:
    type: str
    value: Any | None = None


@dataclass
class AXProperty:
    name: str
    value: AXValue


@dataclass
class AXAndroidNode:
    className: str | None = None
    viewIdResourceName: str | None = None
    packageName: str | None = None
    text: str | None = None
    contentDescription: str | None = None
    hintText: str | None = None


class Type(Enum):
    application = "application"
    inputMethod = "inputMethod"
    system = "system"
    overlay = "overlay"
    other = "other"


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
class TouchTapParams:
    x: int
    y: int
    idempotencyKey: IdempotencyKey | None = None


@dataclass
class TouchLongPressParams:
    x: int
    y: int
    duration_ms: int | None = None
    idempotencyKey: IdempotencyKey | None = None


@dataclass
class TouchSwipeParams:
    x1: int
    y1: int
    x2: int
    y2: int
    duration_ms: int | None = None
    idempotencyKey: IdempotencyKey | None = None


@dataclass
class KeyboardTypeTextParams:
    text: str
    idempotencyKey: IdempotencyKey | None = None


@dataclass
class KeyboardKeyPressParams:
    usage: int | None = None
    key: Key | None = None
    idempotencyKey: IdempotencyKey | None = None


@dataclass
class LocatorPlatform:
    android: AndroidLocator | None = None


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
class LocatorResult:
    resolvedBy: ResolvedBy
    bounds: Bbox
    tookMs: int
    modelName: str | None = None


@dataclass
class LocatorPressResult:
    tookMs: int
    resolvedBy: ResolvedBy | None = None
    bounds: Bbox | None = None
    modelName: str | None = None


@dataclass
class LocatorWaitForResult:
    tookMs: int
    resolvedBy: ResolvedBy | None = None
    bounds: Bbox | None = None
    modelName: str | None = None


@dataclass
class LocatorTextResult:
    text: str
    resolvedBy: ResolvedBy
    bounds: Bbox
    tookMs: int
    modelName: str | None = None


@dataclass
class AXNodePlatform:
    android: AXAndroidNode | None = None


@dataclass
class AXWindow:
    windowId: str
    type: Type
    focused: bool
    bounds: Bbox
    title: str | None = None
    app: str | None = None
    rootId: str | None = None


@dataclass
class Locator:
    role: str | None = None
    name: str | None = None
    text: str | None = None
    exact: bool | None = None
    id: str | None = None
    states: list[str] | None = None
    query: str | None = None
    within: Locator | None = None
    has: Locator | None = None
    nth: int | None = None
    platform: LocatorPlatform | None = None
    value: str | None = None
    windowId: str | None = None
    nodeId: str | None = None


@dataclass
class LocatorTapParams:
    locator: Locator
    strategy: LocatorStrategy | None = None
    timeoutMs: LocatorTimeoutMs | None = 5000
    ocrEngine: LocatorOcrEngine | None = None
    model: LocatorModel | None = None
    idempotencyKey: IdempotencyKey | None = None


@dataclass
class LocatorFillParams:
    locator: Locator
    text: str
    strategy: LocatorStrategy | None = None
    timeoutMs: LocatorTimeoutMs | None = 5000
    ocrEngine: LocatorOcrEngine | None = None
    model: LocatorModel | None = None
    idempotencyKey: IdempotencyKey | None = None


@dataclass
class LocatorPressParams:
    key: Key
    locator: Locator | None = None
    strategy: LocatorStrategy | None = None
    timeoutMs: LocatorTimeoutMs | None = 5000
    ocrEngine: LocatorOcrEngine | None = None
    model: LocatorModel | None = None
    idempotencyKey: IdempotencyKey | None = None


@dataclass
class LocatorWaitForParams:
    locator: Locator
    state: State | None = None
    strategy: LocatorStrategy | None = None
    timeoutMs: LocatorTimeoutMs | None = 5000
    ocrEngine: LocatorOcrEngine | None = None
    model: LocatorModel | None = None


@dataclass
class LocatorQueryParams:
    locator: Locator
    strategy: LocatorStrategy | None = None
    timeoutMs: LocatorTimeoutMs | None = 5000
    ocrEngine: LocatorOcrEngine | None = None
    model: LocatorModel | None = None


@dataclass
class LocatorCountParams:
    locator: Locator
    strategy: LocatorStrategy | None = None
    ocrEngine: LocatorOcrEngine | None = None
    model: LocatorModel | None = None


@dataclass
class QueryAXTreeParams:
    accessibleName: str | None = None
    role: str | None = None
    selector: Locator | None = None


@dataclass
class ObserveResult:
    texts: list[ObserveText]
    icons: list[ObserveIcon]
    hash: str
    width: int
    height: int
    captured_at: int


@dataclass
class AXNode:
    nodeId: str
    ignored: bool
    role: AXValue
    childIds: list[str]
    bounds: Bbox
    windowId: str
    actions: list[str]
    name: AXValue | None = None
    description: AXValue | None = None
    value: AXValue | None = None
    properties: list[AXProperty] | None = None
    parentId: str | None = None
    platform: AXNodePlatform | None = None


@dataclass
class AXTree:
    nodes: list[AXNode]
    windows: list[AXWindow]
    capturedAt: int


@dataclass
class AXNodes:
    nodes: list[AXNode]
