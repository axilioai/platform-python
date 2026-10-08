"""Axilio mobile driver: Locator-based control for a paired device."""

from __future__ import annotations

from ._accessibility import (
    Accessibility,
    AccessibilityState,
    AXAndroidNode,
    AXNode,
    AXProperty,
    AXTree,
    AXValue,
    AXWindow,
)
from ._driver import MobileDriver
from ._errors import (
    ActionTimeoutError,
    AxilioError,
    CanceledError,
    ConnectionError,
    ControlHeldError,
    DeviceOfflineError,
    InternalError,
    InvalidArgsError,
    NoAllocationError,
    NotConnectedError,
    SessionEndedError,
    StaleNodeError,
    StrategyUnavailableError,
    TimeoutError,
    TreeUnavailableError,
    UnauthorizedError,
    UnknownOpError,
)
from ._locator import Locator, LocatorResult, Strategy, WaitState
from ._transport import RemoteTransport, SandboxTransport, Transport
from .keys import Key
from .types import BBox, Coords, DeviceInfo, Element, HandshakeResult, IconBox, Screen

__all__ = [
    "MobileDriver",
    "Transport",
    "SandboxTransport",
    "RemoteTransport",
    "Screen",
    "Element",
    "IconBox",
    "DeviceInfo",
    "HandshakeResult",
    "Locator",
    "LocatorResult",
    "Strategy",
    "WaitState",
    "Accessibility",
    "AccessibilityState",
    "AXTree",
    "AXNode",
    "AXWindow",
    "AXValue",
    "AXProperty",
    "AXAndroidNode",
    "Coords",
    "BBox",
    "Key",
    "AxilioError",
    "ActionTimeoutError",
    "CanceledError",
    "ConnectionError",
    "ControlHeldError",
    "DeviceOfflineError",
    "InternalError",
    "InvalidArgsError",
    "NoAllocationError",
    "NotConnectedError",
    "SessionEndedError",
    "StaleNodeError",
    "StrategyUnavailableError",
    "TimeoutError",
    "TreeUnavailableError",
    "UnauthorizedError",
    "UnknownOpError",
]
