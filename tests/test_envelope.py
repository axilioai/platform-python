"""Wire envelope JSON roundtrip tests. Source of truth for the
serialised shape — if these break, the daemon won't decode our frames
(or vice versa)."""

from __future__ import annotations

import json

from axilio.drivers.mobile import _envelope


def test_command_to_wire_includes_args() -> None:
    cmd = _envelope.Command(id="abc", op="tap", args={"x": 540, "y": 1200})
    assert cmd.to_wire() == {"id": "abc", "op": "tap", "args": {"x": 540, "y": 1200}}


def test_command_to_wire_omits_args_when_none() -> None:
    cmd = _envelope.Command(id="abc", op="screenshot")
    assert cmd.to_wire() == {"id": "abc", "op": "screenshot"}
    assert "args" not in cmd.to_wire()


def test_response_from_wire_ok() -> None:
    raw = {"id": "abc", "ok": True, "result": {"png_base64": "AA=="}}
    resp = _envelope.Response.from_wire(raw)
    assert resp.id == "abc"
    assert resp.ok is True
    assert resp.result == {"png_base64": "AA=="}
    assert resp.error is None


def test_response_from_wire_error() -> None:
    raw = {
        "id": "abc",
        "ok": False,
        "error": {"code": "device_offline", "message": "no driver", "retryable": True},
    }
    resp = _envelope.Response.from_wire(raw)
    assert resp.id == "abc"
    assert resp.ok is False
    assert resp.result is None
    assert resp.error is not None
    assert resp.error.code == "device_offline"
    assert resp.error.message == "no driver"
    assert resp.error.retryable is True


def test_response_from_wire_error_defaults_retryable_false() -> None:
    raw = {"id": "abc", "ok": False, "error": {"code": "internal", "message": "boom"}}
    resp = _envelope.Response.from_wire(raw)
    assert resp.error is not None
    assert resp.error.retryable is False


def test_command_marshal_unmarshal_roundtrip() -> None:
    cmd = _envelope.Command(
        id="01HX", op="swipe", args={"x1": 0, "y1": 0, "x2": 1, "y2": 1, "duration_ms": 300}
    )
    encoded = json.dumps(cmd.to_wire())
    decoded = json.loads(encoded)
    assert decoded == cmd.to_wire()
