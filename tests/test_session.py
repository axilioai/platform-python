"""Remote MobileDriver wiring (AXI-1105): MobileDriver.connect_remote and the
Client.session() allocate -> drive -> release orchestration (+ sandbox shortcut)."""

from __future__ import annotations

import json
from typing import Any

import pytest
import websocket

from axilio._mode import Mode
from axilio.drivers.mobile import MobileDriver
from axilio.platform import AccessibilityUnavailableError, ApiError, Client


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

    # The transport appends its resume opt-in to the attach URL; the
    # caller's token still rides it unchanged.
    assert conns[0].url is not None and "token=abc" in conns[0].url
    assert "resume=1" in conns[0].url
    assert conns[0].sent[0]["method"] == "Touch.tap"
    params = conns[0].sent[0]["params"]
    # Mutating input carries a transport-minted idempotency key beside the
    # caller's own params.
    assert params["x"] == 5 and params["y"] == 6
    assert params["idempotencyKey"]


# --- session() orchestration -------------------------------------------------


class _Alloc:
    def __init__(self, control_url: str | None, phone_id: str, accessibility: bool = True) -> None:
        self.control_url = control_url
        self.phone_id = phone_id
        self.accessibility = accessibility


class _FakePhones:
    def __init__(
        self,
        control_url: str | None = "wss://connect.test/ws?token=x",
        *,
        accessibility: bool = True,
        error: ApiError | None = None,
    ) -> None:
        self._control_url = control_url
        self._accessibility = accessibility
        self._error = error
        self.allocate_calls: list[dict[str, Any]] = []
        self.deallocate_calls: list[str] = []

    def allocate(self, **kwargs: Any) -> _Alloc:
        self.allocate_calls.append(kwargs)
        if self._error is not None:
            raise self._error
        return _Alloc(self._control_url, "phone_123", self._accessibility)

    def deallocate(self, *, phone_id: str) -> None:
        self.deallocate_calls.append(phone_id)


class _FakeApi:
    def __init__(self, phones: _FakePhones) -> None:
        self.phones = phones


class _FakeDriver:
    def __init__(self) -> None:
        self.closed = False

    def close(self) -> None:
        self.closed = True


def _client_with(devices: _FakePhones) -> Client:
    c = Client(api_key="ax_test")
    c._api = _FakeApi(devices)  # type: ignore[assignment]  # noqa: SLF001 — test seam
    return c


def test_session_remote_allocates_drives_releases(monkeypatch: pytest.MonkeyPatch) -> None:
    dev = _FakePhones()
    c = _client_with(dev)
    fake = _FakeDriver()
    monkeypatch.setattr(
        "axilio.platform.MobileDriver.connect_remote",
        classmethod(lambda cls, url, **kw: fake),  # noqa: ARG005
    )
    with c.session("android") as drv:
        assert drv is fake
    # phone_type is sent lowercase to match the Android-only API enum.
    assert dev.allocate_calls == [{"phone_type": "android", "accessibility": True}]
    assert dev.deallocate_calls == ["phone_123"]
    assert fake.closed is True


def test_session_normalizes_android_and_passes_optional_args(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    dev = _FakePhones()
    c = _client_with(dev)
    monkeypatch.setattr(
        "axilio.platform.MobileDriver.connect_remote",
        classmethod(lambda cls, url, **kw: _FakeDriver()),  # noqa: ARG005
    )
    with c.session("ANDROID", phone_id="p1", workflow_id="w1"):  # type: ignore[arg-type]
        pass
    assert dev.allocate_calls == [
        {"phone_type": "android", "accessibility": True, "phone_id": "p1", "workflow_id": "w1"}
    ]


@pytest.mark.parametrize("mode", [Mode.LOCAL, Mode.SANDBOX])
@pytest.mark.parametrize("phone_type", ["iphone", "unknown", ""])
def test_session_rejects_non_android_before_side_effects(
    monkeypatch: pytest.MonkeyPatch,
    mode: Mode,
    phone_type: str,
) -> None:
    dev = _FakePhones()
    c = _client_with(dev)
    c._mode = mode  # noqa: SLF001 — test both execution paths
    monkeypatch.setattr(
        "axilio.platform.MobileDriver.connect",
        classmethod(lambda cls, **kw: _FakeDriver()),  # noqa: ARG005
    )
    monkeypatch.setattr(
        "axilio.platform.MobileDriver.connect_remote",
        classmethod(lambda cls, url, **kw: _FakeDriver()),  # noqa: ARG005
    )

    with (
        pytest.raises(ValueError, match="phone_type must be 'android'"),
        c.session(phone_type),  # type: ignore[arg-type]
    ):
        pass

    assert dev.allocate_calls == []
    assert dev.deallocate_calls == []


def test_session_threads_vision_defaults_to_driver(monkeypatch: pytest.MonkeyPatch) -> None:
    dev = _FakePhones()
    c = _client_with(dev)
    seen_kwargs: dict[str, object] = {}

    def fake_connect_remote(cls, url, **kw):  # noqa: ARG001
        seen_kwargs.update(kw)
        return _FakeDriver()

    monkeypatch.setattr(
        "axilio.platform.MobileDriver.connect_remote", classmethod(fake_connect_remote)
    )
    with c.session("android", default_ocr_engine="premium", default_model="openai/gpt-5"):
        pass
    assert seen_kwargs["default_ocr_engine"] == "premium"
    assert seen_kwargs["default_model"] == "openai/gpt-5"


def test_session_no_control_url_releases_then_raises(monkeypatch: pytest.MonkeyPatch) -> None:
    dev = _FakePhones(control_url=None)
    c = _client_with(dev)
    with pytest.raises(RuntimeError, match="control_url"), c.session("android"):
        pass
    # device was reserved, so it must still be released even though we bailed
    assert dev.deallocate_calls == ["phone_123"]


def test_session_sandbox_skips_allocate(monkeypatch: pytest.MonkeyPatch) -> None:
    dev = _FakePhones()
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


# --- accessibility (AXI-2116) -------------------------------------------------


def _capture_connect_remote(monkeypatch: pytest.MonkeyPatch) -> dict[str, object]:
    seen: dict[str, object] = {}

    def fake_connect_remote(cls, url, **kw):  # noqa: ARG001
        seen.update(kw)
        return _FakeDriver()

    monkeypatch.setattr(
        "axilio.platform.MobileDriver.connect_remote", classmethod(fake_connect_remote)
    )
    return seen


@pytest.mark.parametrize("flag", [True, False])
def test_session_forwards_accessibility_to_allocate(
    monkeypatch: pytest.MonkeyPatch, flag: bool
) -> None:
    dev = _FakePhones(accessibility=flag)
    c = _client_with(dev)
    seen = _capture_connect_remote(monkeypatch)
    with c.session("android", accessibility=flag, default_strategy="vision"):
        pass
    assert dev.allocate_calls == [{"phone_type": "android", "accessibility": flag}]
    # The effective value from the allocate response reaches the driver.
    assert seen["accessibility_at_allocation"] is flag
    assert seen["default_strategy"] == "vision"


def test_session_sends_accessibility_true_by_default(monkeypatch: pytest.MonkeyPatch) -> None:
    dev = _FakePhones()
    c = _client_with(dev)
    seen = _capture_connect_remote(monkeypatch)
    with c.session("android"):
        pass
    assert dev.allocate_calls == [{"phone_type": "android", "accessibility": True}]
    assert seen["accessibility_at_allocation"] is True


def _conflict(detail: str) -> ApiError:
    return ApiError(status_code=409, body={"title": "Conflict", "status": 409, "detail": detail})


def test_session_maps_accessibility_unavailable_409() -> None:
    err = _conflict('accessibility_unavailable: phone "p1" does not support accessibility mode')
    dev = _FakePhones(error=err)
    c = _client_with(dev)
    with (
        pytest.raises(AccessibilityUnavailableError) as info,
        c.session("android", phone_id="p1"),
    ):
        pass
    assert isinstance(info.value, ApiError)
    assert info.value.status_code == 409
    assert info.value.body == err.body
    # Allocate failed, so there is nothing to release.
    assert dev.deallocate_calls == []


def test_session_leaves_other_409s_as_api_error() -> None:
    dev = _FakePhones(error=_conflict('no available device for platform "android"'))
    c = _client_with(dev)
    with pytest.raises(ApiError) as info, c.session("android", accessibility=True):
        pass
    assert not isinstance(info.value, AccessibilityUnavailableError)


def test_phones_allocate_maps_accessibility_unavailable_409() -> None:
    dev = _FakePhones(error=_conflict('accessibility_unavailable: phone "p1" does not support'))
    c = _client_with(dev)
    with pytest.raises(AccessibilityUnavailableError):
        c.phones.allocate(phone_type="android", phone_id="p1", accessibility=True)
    assert dev.allocate_calls == [
        {"phone_type": "android", "phone_id": "p1", "accessibility": True}
    ]
