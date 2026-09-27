"""Axilio mobile driver: Locator-based control for a paired device."""

from __future__ import annotations

from ._driver import MobileDriver
from ._errors import (
    ActionTimeoutError,
    AxilioError,
    CanceledError,
    ConnectionError,
    ControlHeldError,
    DeviceOfflineError,
    ElementNotFoundError,
    InternalError,
    InvalidArgsError,
    NoAllocationError,
    NotConnectedError,
    SessionEndedError,
    StrategyUnavailableError,
    TimeoutError,
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
    "Coords",
    "BBox",
    "Key",
    "AxilioError",
    "ActionTimeoutError",
    "CanceledError",
    "ConnectionError",
    "ControlHeldError",
    "DeviceOfflineError",
    "ElementNotFoundError",
    "InternalError",
    "InvalidArgsError",
    "NoAllocationError",
    "NotConnectedError",
    "SessionEndedError",
    "StrategyUnavailableError",
    "TimeoutError",
    "UnauthorizedError",
    "UnknownOpError",
]
