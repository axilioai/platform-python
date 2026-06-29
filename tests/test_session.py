"""Remote MobileDriver wiring (AXI-1105): MobileDriver.connect_remote and the
Client.session() allocate -> drive -> release orchestration (+ sandbox shortcut)."""

from __future__ import annotations

import json
from typing import Any

import pytest
import websocket

from axilio._mode import Mode
from axilio.drivers.mobile import MobileDriver
from axilio.platform import Client


class FakeWS:
    """Scripted in-memory WebSocket (mirrors test_remote_transport)."""

    def __init__(self, responder: Any) -> None:
        self.responder = responder
        self.sent: list[dict[str, Any]] = []
        self._inbox: list[dict[str, Any]] = []
        self.closed = False
        self.url: str | None = None

    def settimeout(self, _t: float | None) -> None: ...

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


def test_connect_remote_drives_over_cdp() -> None:
    """connect_remote builds a driver whose calls go out as CDP frames over the URL."""
    conns: list[FakeWS] = []

    def connect(url: str, _timeout: float) -> FakeWS:
        ws = FakeWS(lambda f: [{"id": f["id"], "result": {}}])
        ws.url = url
        conns.append(ws)
        return ws

    drv = MobileDriver.connect_remote(
        "wss://connect.test/api/v1/realtime/ws/control?token=abc", connect=connect
    )
    drv.tap({"x": 5, "y": 6})

    assert conns[0].url is not None and conns[0].url.endswith("token=abc")
    assert conns[0].sent[0]["method"] == "Input.tap"
    assert conns[0].sent[0]["params"] == {"x": 5, "y": 6}


# --- session() orchestration -------------------------------------------------


class _Alloc:
    def __init__(self, control_url: str | None, phone_id: str) -> None:
        self.control_url = control_url
        self.phone_id = phone_id


class _FakeDevices:
    def __init__(self, control_url: str | None = "wss://connect.test/ws?token=x") -> None:
        self._control_url = control_url
        self.allocate_calls: list[dict[str, Any]] = []
        self.deallocate_calls: list[str] = []

    def allocate(self, **kwargs: Any) -> _Alloc:
        self.allocate_calls.append(kwargs)
        return _Alloc(self._control_url, "phone_123")

    def deallocate(self, *, phone_id: str) -> None:
        self.deallocate_calls.append(phone_id)


class _FakeApi:
    def __init__(self, devices: _FakeDevices) -> None:
        self.devices = devices


class _FakeDriver:
    def __init__(self) -> None:
        self.closed = False

    def close(self) -> None:
        self.closed = True


def _client_with(devices: _FakeDevices) -> Client:
    c = Client(api_key="ax_test")
    c._api = _FakeApi(devices)  # type: ignore[assignment]  # noqa: SLF001 — test seam
    return c


def test_session_remote_allocates_drives_releases(monkeypatch: pytest.MonkeyPatch) -> None:
    dev = _FakeDevices()
    c = _client_with(dev)
    fake = _FakeDriver()
    monkeypatch.setattr(
        "axilio.platform.MobileDriver.connect_remote",
        classmethod(lambda cls, url, **kw: fake),  # noqa: ARG005
    )
    with c.session("android") as drv:
        assert drv is fake
    assert dev.allocate_calls == [{"phone_type": "android"}]
    assert dev.deallocate_calls == ["phone_123"]
    assert fake.closed is True


def test_session_passes_optional_args(monkeypatch: pytest.MonkeyPatch) -> None:
    dev = _FakeDevices()
    c = _client_with(dev)
    monkeypatch.setattr(
        "axilio.platform.MobileDriver.connect_remote",
        classmethod(lambda cls, url, **kw: _FakeDriver()),  # noqa: ARG005
    )
    with c.session("ios", phone_id="p1", workflow_id="w1"):
        pass
    assert dev.allocate_calls == [{"phone_type": "ios", "phone_id": "p1", "workflow_id": "w1"}]


def test_session_no_control_url_releases_then_raises(monkeypatch: pytest.MonkeyPatch) -> None:
    dev = _FakeDevices(control_url=None)
    c = _client_with(dev)
    with pytest.raises(RuntimeError, match="control_url"), c.session("android"):
        pass
    # device was reserved, so it must still be released even though we bailed
    assert dev.deallocate_calls == ["phone_123"]


def test_session_sandbox_skips_allocate(monkeypatch: pytest.MonkeyPatch) -> None:
    dev = _FakeDevices()
    c = _client_with(dev)
    c._mode = Mode.SANDBOX  # noqa: SLF001 — test seam
    fake = _FakeDriver()
    monkeypatch.setattr(
        "axilio.platform.MobileDriver.connect",
        classmethod(lambda cls, **kw: fake),  # noqa: ARG005
    )
    with c.session("android") as drv:
        assert drv is fake
    assert dev.allocate_calls == []
    assert dev.deallocate_calls == []
    assert fake.closed is True
