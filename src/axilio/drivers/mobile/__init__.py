"""Axilio mobile driver — chainable selector control for a paired device."""

from __future__ import annotations

from ._driver import MobileDriver
from ._errors import (
    AxilioError,
    CanceledError,
    ConnectionError,
    DeviceOfflineError,
    ElementNotFoundError,
    InternalError,
    InvalidArgsError,
    NoAllocationError,
    NotConnectedError,
    TimeoutError,
    UnauthorizedError,
    UnknownOpError,
)
from ._transport import RemoteTransport, SandboxTransport, Transport
from .keys import Key
from .types import BBox, Coords, Element, IconBox, Screen

__all__ = [
    "MobileDriver",
    "Transport",
    "SandboxTransport",
    "RemoteTransport",
    "Screen",
    "Element",
    "IconBox",
    "Coords",
    "BBox",
    "Key",
    "AxilioError",
    "CanceledError",
    "ConnectionError",
    "DeviceOfflineError",
    "ElementNotFoundError",
    "InternalError",
    "InvalidArgsError",
    "NoAllocationError",
    "NotConnectedError",
    "TimeoutError",
    "UnauthorizedError",
    "UnknownOpError",
]
