"""Tests for MobileDriver + the transport seam."""

from __future__ import annotations

import base64
import time
from typing import Any

import pytest

from axilio.drivers.mobile import (
    Element,
    ElementNotFoundError,
    IconBox,
    MobileDriver,
    Screen,
)
from axilio.drivers.mobile import (
    TimeoutError as SdkTimeoutError,
)
from axilio.drivers.mobile._transport import SandboxTransport, Transport


def _driver(daemon: Any) -> MobileDriver:
    return MobileDriver(SandboxTransport(socket_path=daemon.socket_path))


def _ok(cmd: dict[str, Any], result: Any = None) -> dict[str, Any]:
    out: dict[str, Any] = {"id": cmd.get("id", ""), "ok": True}
    if result is not None:
        out["result"] = result
    return out


_OBSERVE_RESULT: dict[str, Any] = {
    "texts": [
        {
            "text": "Sign in",
            "bbox": {"x": 100, "y": 200, "width": 150, "height": 30},
            "confidence": 0.98,
        },
        {
            "text": "Forgot password?",
            "bbox": {"x": 80, "y": 260, "width": 220, "height": 28},
            "confidence": 0.9,
        },
    ],
    "icons": [{"bbox": {"x": 50, "y": 100, "width": 40, "height": 40}, "confidence": 0.95}],
    "hash": "abc123",
    "width": 1080,
    "height": 1920,
    "captured_at": 1780000000000,  # epoch ms (2026-05-28)
}


def test_sandbox_transport_satisfies_transport_protocol() -> None:
    assert isinstance(SandboxTransport(socket_path="/tmp/x.sock"), Transport)


def test_observe_maps_wire_to_screen(fake_daemon: Any) -> None:
    fake_daemon.responder = lambda cmd: _ok(cmd, _OBSERVE_RESULT)
    drv = _driver(fake_daemon)
    try:
        screen = drv.observe(ocr_engine="premium")
    finally:
        drv.close()

    assert isinstance(screen, Screen)
    assert screen.hash == "abc123"
    assert (screen.width, screen.height) == (1080, 1920)
    assert screen.captured_at.year == 2026
    assert len(screen.texts) == 2 and len(screen.icons) == 1

    el = screen.texts[0]
    assert isinstance(el, Element) and el.text == "Sign in" and el.source == "ocr"
    # center = top-left + half-extent
    assert el.center == {"x": 175, "y": 215}
    assert isinstance(screen.icons[0], IconBox)
    assert screen.icons[0].center == {"x": 70, "y": 120}

    obs = next(c for c in fake_daemon.received if c["op"] == "observe")
    assert obs["args"] == {"ocr_engine": "premium"}


def test_find_text_filters_observe(fake_daemon: Any) -> None:
    fake_daemon.responder = lambda cmd: _ok(cmd, _OBSERVE_RESULT)
    drv = _driver(fake_daemon)
    try:
        assert drv.find_text("sign in") is not None  # case-insensitive substring
        assert drv.find_text("Sign In", exact=True) is None  # exact is case-sensitive
        assert drv.find_text("Sign in", exact=True) is not None
        assert drv.find_text("nope") is None
        contains = drv.find_all_text(contains="?")
        assert [e.text for e in contains] == ["Forgot password?"]
    finally:
        drv.close()


def test_find_semantic_found_and_not_found(fake_daemon: Any) -> None:
    def responder(cmd: dict[str, Any]) -> dict[str, Any]:
        if cmd["op"] == "semantic_find":
            if cmd["args"]["query"] == "the buy button":
                return _ok(
                    cmd,
                    {
                        "found": {
                            "bbox": {"x": 200, "y": 300, "width": 100, "height": 50},
                            "confidence": 0.92,
                            "text": "Buy",
                        }
                    },
                )
            return _ok(cmd, {"found": None})
        return _ok(cmd)

    fake_daemon.responder = responder
    drv = _driver(fake_daemon)
    try:
        el = drv.find(query="the buy button")
        assert el.source == "ocr" and el.text == "Buy"
        assert el.center == {"x": 250, "y": 325}
        with pytest.raises(ElementNotFoundError):
            drv.find(query="a unicorn")
    finally:
        drv.close()

    sf = next(c for c in fake_daemon.received if c["op"] == "semantic_find")
    assert sf["args"]["query"] == "the buy button"
    assert sf["args"]["ocr_engine"] == "free"
    assert "model" not in sf["args"]  # omitted when not supplied


def test_find_forwards_model(fake_daemon: Any) -> None:
    fake_daemon.responder = lambda cmd: _ok(cmd, {"found": None})
    drv = _driver(fake_daemon)
    try:
        with pytest.raises(ElementNotFoundError):
            drv.find(query="the buy button", model="openai/gpt-5")
    finally:
        drv.close()

    sf = next(c for c in fake_daemon.received if c["op"] == "semantic_find")
    assert sf["args"]["model"] == "openai/gpt-5"


def test_element_actions_emit_ops_at_center(fake_daemon: Any) -> None:
    def responder(cmd: dict[str, Any]) -> dict[str, Any]:
        if cmd["op"] == "observe":
            return _ok(cmd, _OBSERVE_RESULT)
        return _ok(cmd)

    fake_daemon.responder = responder
    drv = _driver(fake_daemon)
    try:
        screen = drv.observe()
        el = screen.texts[0]  # center (175, 215)
        el.tap()
        el.long_press(duration_ms=500)
        el.type_into("hello")
        el.swipe_to(screen.texts[1])  # other center (190, 274)
    finally:
        drv.close()

    by_op = {c["op"]: c["args"] for c in fake_daemon.received}
    assert by_op["tap"] == {"x": 175, "y": 215}
    assert by_op["long_press"] == {"x": 175, "y": 215, "duration_ms": 500}
    assert by_op["type"] == {"text": "hello"}
    assert by_op["swipe"] == {"x1": 175, "y1": 215, "x2": 190, "y2": 274, "duration_ms": 300}


def test_wait_for_text_polls_until_present(fake_daemon: Any) -> None:
    state = {"n": 0}

    def responder(cmd: dict[str, Any]) -> dict[str, Any]:
        state["n"] += 1
        texts = _OBSERVE_RESULT["texts"] if state["n"] >= 3 else []
        return _ok(cmd, {**_OBSERVE_RESULT, "texts": texts})

    fake_daemon.responder = responder
    drv = _driver(fake_daemon)
    try:
        el = drv.wait_for_text("Sign in", timeout=5, poll_ms=10)
        assert el.text == "Sign in"
        assert state["n"] >= 3
    finally:
        drv.close()


def test_wait_for_text_times_out(fake_daemon: Any) -> None:
    fake_daemon.responder = lambda cmd: _ok(cmd, {**_OBSERVE_RESULT, "texts": []})
    drv = _driver(fake_daemon)
    try:
        with pytest.raises(SdkTimeoutError):
            drv.wait_for_text("Sign in", timeout=0.2, poll_ms=10)
    finally:
        drv.close()


def test_wait_for_predicate(fake_daemon: Any) -> None:
    fake_daemon.responder = lambda cmd: _ok(cmd, _OBSERVE_RESULT)
    drv = _driver(fake_daemon)
    try:
        screen = drv.wait_for(lambda s: s.find_text("Sign in"), timeout=2, poll_ms=10)
        assert isinstance(screen, Screen)
    finally:
        drv.close()


def test_screenshot_decodes_png(fake_daemon: Any) -> None:
    raw = b"\x89PNG\r\n\x1a\n fake"
    fake_daemon.responder = lambda cmd: _ok(cmd, {"png_base64": base64.b64encode(raw).decode()})
    drv = _driver(fake_daemon)
    try:
        assert drv.screenshot() == raw
    finally:
        drv.close()


def test_find_times_out_on_slow_daemon(fake_daemon: Any) -> None:
    def responder(cmd: dict[str, Any]) -> dict[str, Any]:
        time.sleep(0.6)
        return _ok(cmd, {"found": None})

    fake_daemon.responder = responder
    drv = _driver(fake_daemon)
    try:
        with pytest.raises(SdkTimeoutError):
            drv.find(query="anything", timeout=0.2)
    finally:
        drv.close()
