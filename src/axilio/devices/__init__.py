"""Devices — discovery + the acquisition lifecycle (client.mobile.*)."""

from __future__ import annotations

from .handle import DeviceHandle, IceServer
from .resource import MobileResource
from .types import App, AvailableDevice, AvailableDevices, Location, Platform

__all__ = [
    "MobileResource",
    "DeviceHandle",
    "IceServer",
    "AvailableDevices",
    "AvailableDevice",
    "Location",
    "App",
    "Platform",
]
