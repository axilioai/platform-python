"""DCP frame codec tests. Source of truth for the serialised shape —
if these break, the daemon / control WebSocket won't decode our frames
(or vice versa)."""

from __future__ import annotations

import json

import pytest

from axilio.drivers.mobile import _errors
from axilio.drivers.mobile._transport import _build_frame, _decode_frame, _unwrap_reply


def test_build_frame_includes_params() -> None:
    frame = _build_frame(17, "Input.tap", {"x": 540, "y": 1200})
    assert frame == {"id": 17, "method": "Input.tap", "params": {"x": 540, "y": 1200}}


def test_build_frame_omits_params_when_none() -> None:
    frame = _build_frame(3, "Screen.screenshot", None)
    assert frame == {"id": 3, "method": "Screen.screenshot"}
    assert "params" not in frame


def test_frame_marshal_unmarshal_roundtrip() -> None:
    frame = _build_frame(
        42, "Input.swipe", {"x1": 0, "y1": 0, "x2": 1, "y2": 1, "duration_ms": 300}
    )
    assert json.loads(json.dumps(frame)) == frame


def test_decode_frame_rejects_malformed_json() -> None:
    with pytest.raises(_errors.InternalError):
        _decode_frame("{not json")


def test_unwrap_reply_returns_result() -> None:
    assert _unwrap_reply({"id": 1, "result": {"png_base64": "AA=="}}) == {"png_base64": "AA=="}


def test_unwrap_reply_raises_mapped_exception() -> None:
    reply = {
        "id": 1,
        "error": {
            "code": -32004,
            "message": "no driver",
            "data": {"kind": "DeviceOffline", "retryable": True},
        },
    }
    with pytest.raises(_errors.DeviceOfflineError) as exc_info:
        _unwrap_reply(reply)
    assert exc_info.value.message == "no driver"
    assert exc_info.value.retryable is True


def test_unwrap_reply_unknown_kind_degrades_to_internal() -> None:
    reply = {"id": 1, "error": {"code": -1, "message": "??", "data": {"kind": "Exotic"}}}
    with pytest.raises(_errors.InternalError):
        _unwrap_reply(reply)


def test_unwrap_reply_missing_data_degrades_to_internal() -> None:
    reply = {"id": 1, "error": {"code": -32603, "message": "boom"}}
    with pytest.raises(_errors.InternalError) as exc_info:
        _unwrap_reply(reply)
    assert exc_info.value.retryable is False
