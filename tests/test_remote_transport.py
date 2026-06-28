"""Tests for RemoteTransport — the DCP control-WebSocket transport."""

from __future__ import annotations

import json
from collections.abc import Callable
from typing import Any

import pytest
import websocket

from axilio.drivers.mobile import (
    ConnectionError as SdkConnectionError,
)
from axilio.drivers.mobile import (
    DeviceOfflineError,
    ElementNotFoundError,
    MobileDriver,
    RemoteTransport,
)
from axilio.drivers.mobile import (
    TimeoutError as SdkTimeoutError,
)

Responder = Callable[[dict[str, Any]], list[dict[str, Any]]]


class FakeWS:
    """A scripted in-memory WebSocket: each sent frame runs `responder`,
    whose returned frames are queued for subsequent `recv()` calls."""

    def __init__(self, responder: Responder) -> None:
        self.responder = responder
        self.sent: list[dict[str, Any]] = []
        self.timeout: float | None = None
        self.closed = False
        self._inbox: list[dict[str, Any]] = []

    def settimeout(self, t: float | None) -> None:
        self.timeout = t

    def send(self, text: str) -> None:
        frame = json.loads(text)
        self.sent.append(frame)
        self._inbox.extend(self.responder(frame))

    def recv(self) -> str:
        if not self._inbox:
            raise websocket.WebSocketConnectionClosedException("no more frames")
        return json.dumps(self._inbox.pop(0))

    def close(self) -> None:
        self.closed = True


def _reply_result(result: Any) -> Responder:
    return lambda frame: [{"id": frame["id"], "result": result}]


def _transport_with(responder: Responder) -> tuple[RemoteTransport, list[FakeWS]]:
    """Build a RemoteTransport whose connect factory yields fresh FakeWS
    instances (so reconnects are observable)."""
    conns: list[FakeWS] = []

    def connect(_url: str, _timeout: float) -> FakeWS:
        ws = FakeWS(responder)
        conns.append(ws)
        return ws

    return RemoteTransport("wss://connect.test/ws/control?token=x", connect=connect), conns


def test_call_sends_cdp_frame_and_returns_result() -> None:
    rt, conns = _transport_with(_reply_result({"ok": True}))
    out = rt.call("Input.tap", {"x": 540, "y": 1180})
    assert out == {"ok": True}
    assert conns[0].sent[0] == {"id": 1, "method": "Input.tap", "params": {"x": 540, "y": 1180}}


def test_call_omits_params_when_none() -> None:
    rt, conns = _transport_with(_reply_result({"png_base64": "Zg=="}))
    rt.call("Screen.screenshot")
    assert conns[0].sent[0] == {"id": 1, "method": "Screen.screenshot"}


def test_ids_increment_per_call() -> None:
    rt, conns = _transport_with(_reply_result({}))
    rt.call("Input.tap", {"x": 1, "y": 2})
    rt.call("Input.tap", {"x": 3, "y": 4})
    assert [f["id"] for f in conns[0].sent] == [1, 2]


def test_notifications_are_skipped_before_reply() -> None:
    def responder(frame: dict[str, Any]) -> list[dict[str, Any]]:
        return [
            {"method": "Log.entry", "params": {"level": "info"}},  # no id → skipped
            {"id": frame["id"], "result": {"ok": True}},
        ]

    rt, _ = _transport_with(responder)
    assert rt.call("Input.tap", {"x": 1, "y": 2}) == {"ok": True}


def test_error_frame_maps_to_exception() -> None:
    def responder(frame: dict[str, Any]) -> list[dict[str, Any]]:
        return [
            {
                "id": frame["id"],
                "error": {
                    "code": -32004,
                    "message": "device offline",
                    "data": {"kind": "DeviceOffline", "retryable": True},
                },
            }
        ]

    rt, _ = _transport_with(responder)
    with pytest.raises(DeviceOfflineError) as ei:
        rt.call("Input.tap", {"x": 1, "y": 2})
    assert ei.value.retryable is True


def test_element_not_found_kind_maps() -> None:
    def responder(frame: dict[str, Any]) -> list[dict[str, Any]]:
        return [
            {
                "id": frame["id"],
                "error": {
                    "code": -32005,
                    "message": "no match",
                    "data": {"kind": "ElementNotFound"},
                },
            }
        ]

    rt, _ = _transport_with(responder)
    with pytest.raises(ElementNotFoundError):
        rt.call("Screen.find", {"query": "Login"})


def test_timeout_raises_and_reconnects() -> None:
    def responder(_frame: dict[str, Any]) -> list[dict[str, Any]]:
        raise websocket.WebSocketTimeoutException("slow")

    rt, conns = _transport_with(responder)
    with pytest.raises(SdkTimeoutError):
        rt.call("Screen.find", {"query": "x"}, timeout=0.1)
    assert conns[0].closed is True
    # next call must open a fresh connection (the dropped one was closed)
    rt2, conns2 = _transport_with(_reply_result({"ok": True}))
    assert rt2.call("Input.tap", {"x": 1, "y": 1}) == {"ok": True}
    assert len(conns2) == 1


def test_closed_connection_surfaces_connection_error() -> None:
    rt, conns = _transport_with(lambda _frame: [])  # never replies → recv finds empty inbox
    with pytest.raises(SdkConnectionError):
        rt.call("Input.tap", {"x": 1, "y": 2})
    assert conns[0].closed is True


def test_close_is_idempotent() -> None:
    rt, conns = _transport_with(_reply_result({}))
    rt.call("Input.tap", {"x": 1, "y": 2})
    rt.close()
    rt.close()
    assert conns[0].closed is True


def test_driver_over_remote_emits_cdp_methods() -> None:
    """The driver's helpers should put DCP method names on the wire."""
    rt, conns = _transport_with(_reply_result({}))
    drv = MobileDriver(rt)
    drv.tap({"x": 5, "y": 6})
    drv.type_text("hi")
    by_method = {f["method"]: f.get("params") for f in conns[0].sent}
    assert by_method["Input.tap"] == {"x": 5, "y": 6}
    assert by_method["Input.typeText"] == {"text": "hi"}
