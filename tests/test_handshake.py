"""Tests for the DCP capability-negotiation surface (Protocol.handshake / Device.info)."""

from __future__ import annotations

from typing import Any

import pytest

from axilio.drivers.mobile import DeviceInfo, HandshakeResult, MobileDriver
from axilio.drivers.mobile._errors import UnknownOpError
from axilio.drivers.mobile._transport import SandboxTransport


def _driver(daemon: Any) -> MobileDriver:
    return MobileDriver(SandboxTransport(socket_path=daemon.socket_path))


def _ok(cmd: dict[str, Any], result: Any) -> dict[str, Any]:
    return {"id": cmd.get("id", 0), "result": result}


def _err(cmd: dict[str, Any], kind: str, code: int) -> dict[str, Any]:
    return {
        "id": cmd.get("id", 0),
        "error": {"code": code, "message": kind, "data": {"kind": kind}},
    }


_HANDSHAKE_RESULT: dict[str, Any] = {
    "protocol_version": 1,
    "device": {
        "device_id": "p1",
        "platform": "android",
        "form_factor": "phone",
        "input_modalities": ["touch", "keyboard"],
        "screen_width": 1080,
        "screen_height": 2400,
    },
    "domains": ["Device", "Keyboard", "Protocol", "Screen", "Touch"],
    "capabilities": ["Touch.tap", "Screen.observe"],
}


def test_handshake_parses_result(fake_daemon: Any) -> None:
    fake_daemon.responder = lambda cmd: _ok(cmd, _HANDSHAKE_RESULT)
    drv = _driver(fake_daemon)
    try:
        hs = drv.handshake()
    finally:
        drv.close()

    assert isinstance(hs, HandshakeResult)
    assert hs.protocol_version == 1
    assert hs.device.platform == "android" and hs.device.form_factor == "phone"
    assert hs.supports("Touch.tap") and not hs.supports("Pointer.click")
    assert hs.has_domain("Touch") and not hs.has_domain("Pointer")
    sent = next(c for c in fake_daemon.received if c["method"] == "Protocol.handshake")
    assert sent["method"] == "Protocol.handshake"


def test_handshake_propagates_error(fake_daemon: Any) -> None:
    # Every executor implements the handshake, so it is not skew-tolerant: an
    # error (including UnknownOp) propagates rather than being swallowed (AXI-1753).
    fake_daemon.responder = lambda cmd: _err(cmd, "UnknownOp", -32601)
    drv = _driver(fake_daemon)
    try:
        with pytest.raises(UnknownOpError):
            drv.handshake()
    finally:
        drv.close()


def test_device_info_parses(fake_daemon: Any) -> None:
    info_wire = dict(_HANDSHAKE_RESULT["device"], model="Pixel 8", os_version="16")
    fake_daemon.responder = lambda cmd: _ok(cmd, info_wire)
    drv = _driver(fake_daemon)
    try:
        info = drv.device_info()
    finally:
        drv.close()

    assert isinstance(info, DeviceInfo)
    assert info.model == "Pixel 8"
    assert info.input_modalities == ("touch", "keyboard")
