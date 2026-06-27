"""DeviceHandle — an acquired device, returned by client.mobile.allocate()."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import TYPE_CHECKING, Any, Literal

if TYPE_CHECKING:
    from .resource import MobileResource


@dataclass(frozen=True)
class IceServer:
    """One STUN/TURN server credential, pre-minted by the backend."""

    urls: list[str]
    username: str | None
    credential: str | None


@dataclass(frozen=True)
class DeviceHandle:
    """An active device allocation that a driver can wrap (also its Transport seam)."""

    id: str
    device_id: str
    device_name: str
    platform: Literal["android", "iphone"]
    location: str
    expires_at: datetime
    signaling_url: str
    signaling_token: str
    ice_servers: list[IceServer]
    _resource: MobileResource = field(repr=False, compare=False)

    def call(
        self,
        op: str,
        args: dict[str, Any] | None = None,
        *,
        timeout: float | None = None,
    ) -> dict[str, Any] | None:
        """Send one control-op to the device's on-device agent (local transport not wired yet)."""
        raise NotImplementedError(
            "Driving an allocated device from outside a sandbox needs the "
            "local transport (a WebSocket channel to the on-device agent), "
            "which isn't wired yet. Inside a sandbox, use MobileDriver.connect()."
        )

    def close(self) -> None:
        """Close the transport (no-op until the local transport lands)."""

    def deallocate(self) -> None:
        """Release the device and end billing."""
        self._resource.deallocate(self.id)

    def __enter__(self) -> DeviceHandle:
        return self

    def __exit__(self, *_: object) -> None:
        self.deallocate()
