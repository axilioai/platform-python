"""client.mobile + DeviceHandle wiring."""

from __future__ import annotations

from datetime import datetime, timezone

import pytest

from axilio.devices import DeviceHandle, IceServer, MobileResource
from axilio.platform import Client


def test_mobile_resource_attached() -> None:
    with Client(api_key="ax_test") as client:
        assert isinstance(client.mobile, MobileResource)


def _make_handle(resource: object) -> DeviceHandle:
    return DeviceHandle(
        id="alloc_123",
        device_id="dev_abc",
        device_name="Pixel 8",
        platform="android",
        location="us-east-1a",
        expires_at=datetime(2026, 1, 1, tzinfo=timezone.utc),
        signaling_url="wss://atlas.example/signal",
        signaling_token="tok_xyz",
        ice_servers=[IceServer(urls=["stun:stun.example:3478"], username=None, credential=None)],
        _resource=resource,  # type: ignore[arg-type]
    )


def test_handle_is_transport_seam() -> None:
    """call() raises until the local transport lands; close() is a safe no-op."""
    handle = _make_handle(resource=object())
    with pytest.raises(NotImplementedError):
        handle.call("tap", {"x": 1, "y": 2})
    handle.close()


def test_handle_eq_ignores_resource() -> None:
    """Two handles for the same allocation compare equal (resource excluded from eq)."""
    assert _make_handle(object()) == _make_handle(object())


def test_context_manager_deallocates_once() -> None:
    calls: list[str] = []

    class _Recorder:
        def deallocate(self, allocation_id: str) -> None:
            calls.append(allocation_id)

    handle = _make_handle(_Recorder())
    with handle as device:
        assert device is handle
    assert calls == ["alloc_123"]


def test_allocate_pending() -> None:
    """allocate() is a stub until codegen + the sandbox shortcut land."""
    with Client(api_key="ax_test") as client, pytest.raises(NotImplementedError):
        client.mobile.allocate(platform="android")
