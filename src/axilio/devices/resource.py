"""MobileResource — client.mobile.*"""

from __future__ import annotations

from collections.abc import Iterator
from contextlib import contextmanager

from .._resource import _Resource
from .handle import DeviceHandle
from .types import App, AvailableDevices, Location, Platform


class MobileResource(_Resource):
    """client.mobile — discover, allocate, and release devices."""

    def available(
        self,
        *,
        platform: Platform | None = None,
        location: str | None = None,
        apps: list[str] | None = None,
    ) -> AvailableDevices:
        """List free devices matching the filter."""
        raise NotImplementedError("MobileResource.available — codegen pending")

    def locations(self) -> list[Location]:
        """List rack / data-center locations devices can be pinned to."""
        raise NotImplementedError("MobileResource.locations — codegen pending")

    def supported_apps(
        self,
        *,
        platform: Platform | None = None,
        category: str | None = None,
    ) -> list[App]:
        """List apps available on the fleet."""
        raise NotImplementedError("MobileResource.supported_apps — codegen pending")

    def allocate(
        self,
        *,
        platform: Platform = "android",
        location: str | None = None,
        apps: list[str] | None = None,
        timeout: float = 60.0,
    ) -> DeviceHandle:
        """Acquire a device and return a `DeviceHandle` to wrap with a driver."""
        raise NotImplementedError("MobileResource.allocate — codegen + sandbox-shortcut pending")

    def deallocate(self, allocation_id: str) -> None:
        """Release an allocation (no-op in sandbox mode)."""
        raise NotImplementedError("MobileResource.deallocate — codegen pending")

    @contextmanager
    def session(
        self,
        *,
        platform: Platform = "android",
        location: str | None = None,
        apps: list[str] | None = None,
        timeout: float = 60.0,
    ) -> Iterator[DeviceHandle]:
        """All-in-one: allocate → yield the handle → deallocate."""
        device = self.allocate(platform=platform, location=location, apps=apps, timeout=timeout)
        try:
            yield device
        finally:
            device.deallocate()
