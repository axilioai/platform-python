"""Public dataclasses for device discovery."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

Platform = Literal["android", "iphone"]


@dataclass(frozen=True)
class App:
    """A supported app on the fleet, indexed by bundle id."""

    bundle_id: str
    name: str
    platform: Platform
    category: str | None


@dataclass(frozen=True)
class Location:
    """A rack / data-center location."""

    id: str
    name: str
    region: str


@dataclass(frozen=True)
class AvailableDevice:
    """One free device matching the discovery filter, not yet allocated."""

    id: str
    name: str
    platform: Platform
    location: Location
    model: str
    os_version: str


@dataclass(frozen=True)
class AvailableDevices:
    """Result of mobile.available(...) — the matching set plus the fleet total."""

    devices: list[AvailableDevice]
    total_in_fleet: int
