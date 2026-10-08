"""Tests for MobileDriver + the transport seam."""

from __future__ import annotations

import base64
import socket
import time
from datetime import datetime, timezone
from typing import Any

import pytest

from axilio.drivers.mobile import (
    ActionTimeoutError,
    Element,
    IconBox,
    Key,
    Locator,
    LocatorResult,
    MobileDriver,
    Screen,
    StrategyUnavailableError,
)
from axilio.drivers.mobile import (
    ConnectionError as SdkConnectionError,
)
from axilio.drivers.mobile import (
    TimeoutError as SdkTimeoutError,
)
from axilio.drivers.mobile import _driver as driver_module
from axilio.drivers.mobile._transport import SandboxTransport, Transport


def _driver(daemon: Any, **kwargs: Any) -> MobileDriver:
    return MobileDriver(SandboxTransport(socket_path=daemon.socket_path), **kwargs)


def _ok(cmd: dict[str, Any], result: Any = None) -> dict[str, Any]:
    # CDP success always carries a result — {} for void commands.
    return {"id": cmd.get("id", 0), "result": result if result is not None else {}}


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

_LOCATOR_RESULT: dict[str, Any] = {
    "resolvedBy": "ocr",
    "bounds": {"x": 100, "y": 200, "width": 150, "height": 30},
    "tookMs": 42,
}


def test_sandbox_transport_satisfies_transport_protocol() -> None:
    assert isinstance(SandboxTransport(socket_path="/tmp/x.sock"), Transport)


def test_sandbox_transport_without_unix_sockets_raises_connection_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    # CPython on Windows has no socket.AF_UNIX.
    monkeypatch.delattr(socket, "AF_UNIX", raising=False)
    transport = SandboxTransport(socket_path="/tmp/x.sock")
    with pytest.raises(SdkConnectionError, match="only runs inside an Axilio sandbox"):
        transport.call("Screen.observe")


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

    obs = next(c for c in fake_daemon.received if c["method"] == "Screen.observe")
    assert obs["params"] == {"ocr_engine": "premium"}


def test_observe_defaults_ocr_engine_to_free(fake_daemon: Any) -> None:
    fake_daemon.responder = lambda cmd: _ok(cmd, _OBSERVE_RESULT)
    drv = _driver(fake_daemon)
    try:
        drv.observe()
    finally:
        drv.close()

    obs = next(c for c in fake_daemon.received if c["method"] == "Screen.observe")
    assert obs["params"]["ocr_engine"] == "free"


def test_screen_find_text_and_find_all_text_are_pure_data_filters() -> None:
    # Element / Screen carry no driver reference; these are plain filters
    # over one already-captured observation, unrelated to the transport.
    screen = Screen(
        texts=[
            Element(
                bbox={"x": 0, "y": 0, "width": 10, "height": 10},
                center={"x": 5, "y": 5},
                confidence=0.9,
                text="Sign in",
                source="ocr",
            ),
            Element(
                bbox={"x": 0, "y": 20, "width": 10, "height": 10},
                center={"x": 5, "y": 25},
                confidence=0.9,
                text="Forgot password?",
                source="ocr",
            ),
        ],
        icons=[],
        hash="h",
        width=100,
        height=100,
        captured_at=datetime.now(tz=timezone.utc),
    )
    assert screen.find_text("sign in") is not None  # case-insensitive substring
    assert screen.find_text("Sign In", exact=True) is None  # exact is case-sensitive
    assert screen.find_text("Sign in", exact=True) is not None
    assert screen.find_text("nope") is None
    assert [e.text for e in screen.find_all_text(contains="?")] == ["Forgot password?"]


def test_screenshot_decodes_png(fake_daemon: Any) -> None:
    raw = b"\x89PNG\r\n\x1a\n fake"
    fake_daemon.responder = lambda cmd: _ok(cmd, {"png_base64": base64.b64encode(raw).decode()})
    drv = _driver(fake_daemon)
    try:
        assert drv.screenshot() == raw
    finally:
        drv.close()


def test_stale_reply_from_abandoned_call_is_skipped(fake_daemon: Any) -> None:
    # An interrupted call can leave its reply queued on the socket; the
    # transport must skip stale lower-id frames and match its own id.
    def responder(cmd: dict[str, Any]) -> Any:
        rid = cmd.get("id", 0)
        if rid == 2:
            return [{"id": 1, "result": {}}, {"id": 2, "result": {"png_base64": "AA=="}}]
        return {"id": rid, "result": {}}

    fake_daemon.responder = responder
    transport = SandboxTransport(socket_path=fake_daemon.socket_path)
    try:
        assert transport.call("Touch.tap", {"x": 1, "y": 1}) == {}
        assert transport.call("Screen.screenshot") == {"png_base64": "AA=="}
    finally:
        transport.close()


def test_interrupted_call_drops_connection(fake_daemon: Any) -> None:
    # A notebook cell cancel raises KeyboardInterrupt mid-recv; the
    # transport must close the socket so the abandoned call's late reply
    # can't be misread as the next call's (AXI-1142).
    transport = SandboxTransport(socket_path=fake_daemon.socket_path)
    try:
        assert transport.call("Touch.tap", {"x": 1, "y": 1}) == {}

        def interrupted_recv() -> dict[str, Any]:
            raise KeyboardInterrupt

        transport._recv = interrupted_recv  # type: ignore[method-assign]
        with pytest.raises(KeyboardInterrupt):
            transport.call("Touch.tap", {"x": 2, "y": 2})
        assert transport._sock is None  # connection dropped

        del transport.__dict__["_recv"]  # restore the real method
        # Reconnects lazily on a fresh socket; ids keep counting up and the
        # abandoned id 2's reply died with the old connection.
        assert transport.call("Screen.screenshot") == {}
    finally:
        transport.close()


def test_key_press_sends_named_key(fake_daemon: Any) -> None:
    # AXI-1145: key_press speaks named keys ({"key": "enter"}), not the
    # old consumer-page usage ints.
    drv = _driver(fake_daemon)
    try:
        drv.key_press(Key.ENTER)
    finally:
        drv.close()

    kp = next(c for c in fake_daemon.received if c["method"] == "Keyboard.keyPress")
    assert kp["params"] == {"key": "enter"}


# --- Locator ------------------------------------------------------------


def test_locator_is_lazy_and_sends_nothing_until_an_action(fake_daemon: Any) -> None:
    drv = _driver(fake_daemon)
    try:
        drv.get_by_text("Continue")
        drv.get_by_role("button", name="Save")
        drv.get_by_id("com.example.app:id/save")
        loc = drv.locator(query="the blue save button")
        loc.nth(2).first().filter(query="the cheapest one")
        loc.within(drv.get_by_text("Card")).has(drv.get_by_text("Free shipping"))
    finally:
        drv.close()

    assert fake_daemon.received == []


def test_get_by_text_tap_wire_shape(fake_daemon: Any) -> None:
    fake_daemon.responder = lambda cmd: _ok(cmd, _LOCATOR_RESULT)
    drv = _driver(fake_daemon)
    try:
        result = drv.get_by_text("Continue").tap()
    finally:
        drv.close()

    cmd = next(c for c in fake_daemon.received if c["method"] == "Locator.tap")
    assert cmd["params"] == {"locator": {"text": "Continue", "exact": False}}
    assert result == LocatorResult(
        resolved_by="ocr",
        bounds={"x": 100, "y": 200, "width": 150, "height": 30},
        took_ms=42,
        model_name=None,
    )


def test_get_by_role_and_get_by_id_wire_shape(fake_daemon: Any) -> None:
    fake_daemon.responder = lambda cmd: _ok(cmd, _LOCATOR_RESULT)
    drv = _driver(fake_daemon)
    try:
        drv.get_by_role("button", name="Save").tap()
        drv.get_by_id("com.example.app:id/save").tap()
        drv.get_by_role("checkbox", name="remember", exact=True, states=["checked"]).tap()
    finally:
        drv.close()

    taps = [c for c in fake_daemon.received if c["method"] == "Locator.tap"]
    assert taps[0]["params"] == {"locator": {"role": "button", "name": "Save"}}
    assert taps[1]["params"] == {"locator": {"id": "com.example.app:id/save"}}
    assert taps[2]["params"] == {
        "locator": {"role": "checkbox", "name": "remember", "exact": True, "states": ["checked"]}
    }


def test_locator_tree_fields_go_out_camel_case(fake_daemon: Any) -> None:
    fake_daemon.responder = lambda cmd: _ok(cmd, _LOCATOR_RESULT)
    drv = _driver(fake_daemon)
    try:
        drv.locator(
            role="textbox",
            value="me@",
            window_id="w1",
            node_id="n42",
            android_class_name="android.widget.EditText",
            package_name="com.example.app",
        ).tap()
        drv.locator(package_name="com.example.app").tap()
    finally:
        drv.close()

    taps = [c for c in fake_daemon.received if c["method"] == "Locator.tap"]
    assert taps[0]["params"] == {
        "locator": {
            "role": "textbox",
            "value": "me@",
            "windowId": "w1",
            "nodeId": "n42",
            "platform": {
                "android": {
                    "className": "android.widget.EditText",
                    "packageName": "com.example.app",
                }
            },
        }
    }
    assert taps[1]["params"] == {
        "locator": {"platform": {"android": {"packageName": "com.example.app"}}}
    }


def test_locator_fill_sends_text(fake_daemon: Any) -> None:
    fake_daemon.responder = lambda cmd: _ok(cmd, _LOCATOR_RESULT)
    drv = _driver(fake_daemon)
    try:
        drv.get_by_text("Email").fill("me@example.com")
    finally:
        drv.close()

    cmd = next(c for c in fake_daemon.received if c["method"] == "Locator.fill")
    assert cmd["params"] == {
        "locator": {"text": "Email", "exact": False},
        "text": "me@example.com",
    }


def test_locator_press_and_driver_level_press(fake_daemon: Any) -> None:
    fake_daemon.responder = lambda cmd: _ok(cmd, {"tookMs": 7})
    drv = _driver(fake_daemon)
    try:
        drv.get_by_text("Search").press(Key.ENTER)
        result = drv.press(Key.ENTER)
    finally:
        drv.close()

    presses = [c for c in fake_daemon.received if c["method"] == "Locator.press"]
    assert presses[0]["params"] == {"locator": {"text": "Search", "exact": False}, "key": "enter"}
    # Driver-level press carries no locator at all; it targets the focused
    # element, not something resolved on screen.
    assert presses[1]["params"] == {"key": "enter"}
    assert result == LocatorResult(resolved_by=None, bounds=None, took_ms=7, model_name=None)


def test_locator_refinements_build_expected_spec(fake_daemon: Any) -> None:
    fake_daemon.responder = lambda cmd: _ok(cmd, _LOCATOR_RESULT)
    drv = _driver(fake_daemon)
    try:
        card = drv.get_by_text("Card")
        drv.locator(query="a list item").within(card).has(drv.get_by_text("Free shipping")).nth(
            1
        ).filter(query="the cheapest one").tap()
    finally:
        drv.close()

    cmd = next(c for c in fake_daemon.received if c["method"] == "Locator.tap")
    assert cmd["params"]["locator"] == {
        "query": "a list item, the cheapest one",
        "within": {"text": "Card", "exact": False},
        "has": {"text": "Free shipping", "exact": False},
        "nth": 1,
    }


def test_locator_wait_for_visible_and_hidden(fake_daemon: Any) -> None:
    fake_daemon.responder = lambda cmd: _ok(cmd, _LOCATOR_RESULT)
    drv = _driver(fake_daemon)
    try:
        visible = drv.get_by_text("Welcome").wait_for()
        gone = drv.get_by_text("Loading").wait_for(state="hidden")
    finally:
        drv.close()

    assert visible is not None and visible.resolved_by == "ocr"
    assert gone is None

    calls = [c for c in fake_daemon.received if c["method"] == "Locator.waitFor"]
    assert "state" not in calls[0]["params"]  # visible is the wire default, omitted
    assert calls[1]["params"]["state"] == "hidden"


def test_locator_bounding_box_and_text_and_count(fake_daemon: Any) -> None:
    def responder(cmd: dict[str, Any]) -> dict[str, Any]:
        if cmd["method"] == "Locator.text":
            return _ok(cmd, {**_LOCATOR_RESULT, "text": "Sign in"})
        if cmd["method"] == "Locator.count":
            return _ok(cmd, {"count": 3, "resolvedBy": "ocr", "tookMs": 1})
        return _ok(cmd, _LOCATOR_RESULT)

    fake_daemon.responder = responder
    drv = _driver(fake_daemon)
    try:
        loc = drv.get_by_text("Sign in")
        box = loc.bounding_box()
        text = loc.text()
        count = loc.count(timeout=1.0)
    finally:
        drv.close()

    assert box.bounds == {"x": 100, "y": 200, "width": 150, "height": 30}
    assert text == "Sign in"
    assert count == 3

    count_cmd = next(c for c in fake_daemon.received if c["method"] == "Locator.count")
    assert "timeoutMs" not in count_cmd["params"]  # Locator.count has no timeoutMs on the wire


def test_locator_defaults_apply_when_call_omits_them(fake_daemon: Any) -> None:
    fake_daemon.responder = lambda cmd: _ok(cmd, _LOCATOR_RESULT)
    drv = _driver(
        fake_daemon,
        default_ocr_engine="premium",
        default_model="openai/gpt-5",
    )
    try:
        drv.get_by_text("Sign in").tap()
    finally:
        drv.close()

    cmd = next(c for c in fake_daemon.received if c["method"] == "Locator.tap")
    assert cmd["params"]["ocrEngine"] == "premium"
    assert cmd["params"]["model"] == "openai/gpt-5"
    assert "strategy" not in cmd["params"]


def test_locator_constructor_arguments_override_driver_defaults(fake_daemon: Any) -> None:
    fake_daemon.responder = lambda cmd: _ok(cmd, _LOCATOR_RESULT)
    drv = _driver(
        fake_daemon,
        default_ocr_engine="premium",
        default_model="openai/gpt-5",
    )
    try:
        drv.get_by_text("Sign in", ocr_engine="free", model="google/gemini-3-flash").tap()
    finally:
        drv.close()

    cmd = next(c for c in fake_daemon.received if c["method"] == "Locator.tap")
    assert cmd["params"]["ocrEngine"] == "free"
    assert cmd["params"]["model"] == "google/gemini-3-flash"
    assert "strategy" not in cmd["params"]


def test_locator_refinement_keeps_the_receivers_options(fake_daemon: Any) -> None:
    # nth/first/filter return a new Locator that keeps whatever the receiver
    # was built with; the option isn't repeated at the refinement call.
    fake_daemon.responder = lambda cmd: _ok(cmd, _LOCATOR_RESULT)
    drv = _driver(fake_daemon)
    try:
        drv.get_by_text("Item", model="openai/gpt-5").nth(1).tap()
    finally:
        drv.close()

    cmd = next(c for c in fake_daemon.received if c["method"] == "Locator.tap")
    assert cmd["params"]["model"] == "openai/gpt-5"


def test_within_and_has_raise_when_inner_locator_sets_an_option(fake_daemon: Any) -> None:
    # A locator passed into within()/has() contributes only its selector;
    # the outer locator's options govern the whole call, so an inner locator
    # that sets model/ocr_engine on itself is a build-time error rather than
    # a silently ignored option.
    drv = _driver(fake_daemon)
    try:
        outer = drv.get_by_text("Save", model="openai/gpt-5")

        with pytest.raises(ValueError, match="within.*model"):
            outer.within(drv.get_by_text("Card", model="openai/gpt-5"))
        with pytest.raises(ValueError, match="within.*ocr_engine"):
            outer.within(drv.get_by_text("Card", ocr_engine="premium"))

        with pytest.raises(ValueError, match="has.*model"):
            outer.has(drv.get_by_text("Free shipping", model="openai/gpt-5"))
        with pytest.raises(ValueError, match="has.*ocr_engine"):
            outer.has(drv.get_by_text("Free shipping", ocr_engine="premium"))
    finally:
        drv.close()

    assert fake_daemon.received == []


def test_within_and_has_accept_inner_locator_with_no_options(fake_daemon: Any) -> None:
    # An inner locator that sets no options of its own still works: only its
    # selector fields become the within/has scope.
    fake_daemon.responder = lambda cmd: _ok(cmd, _LOCATOR_RESULT)
    drv = _driver(fake_daemon)
    try:
        inner = drv.get_by_text("Card")
        drv.get_by_text("Save", model="openai/gpt-5").within(inner).tap()
    finally:
        drv.close()

    cmd = next(c for c in fake_daemon.received if c["method"] == "Locator.tap")
    assert cmd["params"]["model"] == "openai/gpt-5"
    assert "ocrEngine" not in cmd["params"]
    assert cmd["params"]["locator"]["within"] == {"text": "Card", "exact": False}


def test_within_and_has_ignore_driver_defaults_on_the_inner_locator(fake_daemon: Any) -> None:
    # Driver defaults are applied later, at call time, and never land on the
    # inner locator's own model/ocr_engine attributes, so a driver with
    # defaults set does not trip the inner-options check.
    fake_daemon.responder = lambda cmd: _ok(cmd, _LOCATOR_RESULT)
    drv = _driver(
        fake_daemon,
        default_model="openai/gpt-5",
        default_ocr_engine="premium",
    )
    try:
        inner = drv.get_by_text("Card")
        drv.get_by_text("Save").within(inner).has(drv.get_by_text("Free shipping")).tap()
    finally:
        drv.close()

    cmd = next(c for c in fake_daemon.received if c["method"] == "Locator.tap")
    assert cmd["params"]["model"] == "openai/gpt-5"
    assert cmd["params"]["ocrEngine"] == "premium"
    assert "strategy" not in cmd["params"]
    assert cmd["params"]["locator"]["within"] == {"text": "Card", "exact": False}
    assert cmd["params"]["locator"]["has"] == {"text": "Free shipping", "exact": False}


def test_locator_omits_strategy_model_ocr_engine_when_unset(fake_daemon: Any) -> None:
    # A Locator call with nothing set on either side leaves strategy/model/
    # ocrEngine off the wire so the server's own defaults apply.
    fake_daemon.responder = lambda cmd: _ok(cmd, _LOCATOR_RESULT)
    drv = _driver(fake_daemon)
    try:
        drv.get_by_text("Sign in").tap()
    finally:
        drv.close()

    cmd = next(c for c in fake_daemon.received if c["method"] == "Locator.tap")
    assert "strategy" not in cmd["params"]
    assert "model" not in cmd["params"]
    assert "ocrEngine" not in cmd["params"]
    assert "timeoutMs" not in cmd["params"]


def test_strategy_flows_from_driver_default_and_call_override(fake_daemon: Any) -> None:
    fake_daemon.responder = lambda cmd: _ok(cmd, _LOCATOR_RESULT)
    drv = _driver(fake_daemon, default_strategy="vision")
    try:
        drv.locator(query="the log in button").tap()
        drv.get_by_role("button", strategy="accessibility").tap()
    finally:
        drv.close()

    taps = [c for c in fake_daemon.received if c["method"] == "Locator.tap"]
    assert taps[0]["params"]["strategy"] == "vision"
    assert taps[1]["params"]["strategy"] == "accessibility"


def test_locator_refinement_keeps_strategy(fake_daemon: Any) -> None:
    fake_daemon.responder = lambda cmd: _ok(cmd, _LOCATOR_RESULT)
    drv = _driver(fake_daemon)
    try:
        drv.get_by_id("save", strategy="accessibility").nth(1).tap()
    finally:
        drv.close()

    cmd = next(c for c in fake_daemon.received if c["method"] == "Locator.tap")
    assert cmd["params"]["strategy"] == "accessibility"


def test_within_and_has_raise_when_inner_locator_sets_strategy(fake_daemon: Any) -> None:
    drv = _driver(fake_daemon)
    try:
        outer = drv.get_by_role("listitem")
        with pytest.raises(ValueError, match="within.*strategy"):
            outer.within(drv.get_by_id("card", strategy="vision"))
        with pytest.raises(ValueError, match="has.*strategy"):
            outer.has(drv.get_by_id("shipping", strategy="vision"))
    finally:
        drv.close()

    assert fake_daemon.received == []


def test_wait_for_enabled_state(fake_daemon: Any) -> None:
    fake_daemon.responder = lambda cmd: _ok(cmd, _LOCATOR_RESULT)
    drv = _driver(fake_daemon)
    try:
        result = drv.get_by_id("toggle").wait_for(state="enabled")
    finally:
        drv.close()

    cmd = next(c for c in fake_daemon.received if c["method"] == "Locator.waitFor")
    assert cmd["params"]["state"] == "enabled"
    assert result is not None


def test_driver_level_press_sends_no_resolution_options(fake_daemon: Any) -> None:
    # Driver-level press() has no locator to resolve, so it never sends
    # model/ocrEngine, even when the driver has defaults set (and it never
    # sends strategy regardless).
    fake_daemon.responder = lambda cmd: _ok(cmd, {"tookMs": 7})
    drv = _driver(
        fake_daemon,
        default_ocr_engine="premium",
        default_model="openai/gpt-5",
    )
    try:
        drv.press(Key.ENTER)
    finally:
        drv.close()

    cmd = next(c for c in fake_daemon.received if c["method"] == "Locator.press")
    assert cmd["params"] == {"key": "enter"}


def test_locator_timeout_becomes_timeout_ms(fake_daemon: Any) -> None:
    fake_daemon.responder = lambda cmd: _ok(cmd, _LOCATOR_RESULT)
    drv = _driver(fake_daemon)
    try:
        drv.get_by_text("Sign in").tap(timeout=2.5)
    finally:
        drv.close()

    cmd = next(c for c in fake_daemon.received if c["method"] == "Locator.tap")
    assert cmd["params"]["timeoutMs"] == 2500


def test_locator_timeout_out_of_range_raises(fake_daemon: Any) -> None:
    drv = _driver(fake_daemon)
    try:
        with pytest.raises(ValueError):
            drv.get_by_text("Sign in").tap(timeout=61)
    finally:
        drv.close()


def test_locator_transport_timeout_exceeds_device_budget(
    fake_daemon: Any, monkeypatch: Any
) -> None:
    # The SDK's own call must outlast timeoutMs by the contract's margin (an
    # inference already running when the budget ends is allowed to finish);
    # shrink the margin so the test doesn't have to wait out the real one.
    monkeypatch.setattr(driver_module, "_LOCATOR_TRANSPORT_MARGIN_S", 0.5)

    def responder(cmd: dict[str, Any]) -> dict[str, Any]:
        time.sleep(0.2)
        return _ok(cmd, _LOCATOR_RESULT)

    fake_daemon.responder = responder
    drv = _driver(fake_daemon)
    try:
        # timeoutMs=100 + margin 500ms = 600ms transport budget, comfortably
        # more than the 200ms the fake device takes.
        result = drv.get_by_text("Sign in").tap(timeout=0.1)
    finally:
        drv.close()
    assert result.resolved_by == "ocr"


def test_locator_slow_daemon_past_transport_budget_times_out(
    fake_daemon: Any, monkeypatch: Any
) -> None:
    monkeypatch.setattr(driver_module, "_LOCATOR_TRANSPORT_MARGIN_S", 0.1)

    def responder(cmd: dict[str, Any]) -> dict[str, Any]:
        time.sleep(0.4)
        return _ok(cmd, _LOCATOR_RESULT)

    fake_daemon.responder = responder
    drv = _driver(fake_daemon)
    try:
        # timeoutMs=50 + margin 100ms = 150ms transport budget; the fake
        # device takes 400ms, well past it.
        with pytest.raises(SdkTimeoutError):
            drv.get_by_text("Sign in").tap(timeout=0.05)
    finally:
        drv.close()


def test_action_timeout_error_maps_and_matches_builtin_timeout(fake_daemon: Any) -> None:
    def responder(cmd: dict[str, Any]) -> dict[str, Any]:
        return {
            "id": cmd["id"],
            "error": {
                "code": -32009,
                "message": "target never became actionable",
                "data": {"kind": "ActionTimeout", "retryable": False},
            },
        }

    fake_daemon.responder = responder
    drv = _driver(fake_daemon)
    try:
        with pytest.raises(ActionTimeoutError) as ei:
            drv.get_by_text("Sign in").tap()
    finally:
        drv.close()
    assert isinstance(ei.value, TimeoutError)  # the builtin, not the SDK's own


def test_strategy_unavailable_error_maps(fake_daemon: Any) -> None:
    def responder(cmd: dict[str, Any]) -> dict[str, Any]:
        return {
            "id": cmd["id"],
            "error": {
                "code": -32010,
                "message": "no accessibility tree on this session",
                "data": {"kind": "StrategyUnavailable"},
            },
        }

    fake_daemon.responder = responder
    drv = _driver(fake_daemon)
    try:
        with pytest.raises(StrategyUnavailableError):
            drv.get_by_text("Sign in").tap()
    finally:
        drv.close()


def test_locator_is_immutable_refinement_leaves_receiver_unchanged(fake_daemon: Any) -> None:
    fake_daemon.responder = lambda cmd: _ok(cmd, _LOCATOR_RESULT)
    drv = _driver(fake_daemon)
    try:
        base = drv.get_by_text("Item")
        refined = base.nth(2)
        assert refined is not base
        assert isinstance(refined, Locator)
        base.tap()
    finally:
        drv.close()

    cmd = next(c for c in fake_daemon.received if c["method"] == "Locator.tap")
    assert "nth" not in cmd["params"]["locator"]


def test_refinements_only_narrow(fake_daemon: Any) -> None:
    # A second within keeps the first scope (chained, not replaced), a second
    # filter appends its query, and the receiver is unchanged.
    driver = _driver(fake_daemon)
    base = driver.get_by_text("Save")
    loc = (
        base.within(driver.get_by_text("Dialog"))
        .within(driver.get_by_text("Card"))
        .filter(query="the primary one")
        .filter(query="enabled")
    )
    spec = loc._spec
    assert spec["within"]["text"] == "Card"
    assert spec["within"]["within"]["text"] == "Dialog"
    assert spec["query"] == "the primary one, enabled"
    assert "within" not in base._spec and "query" not in base._spec


def test_count_timeout_is_the_whole_deadline(fake_daemon: Any, monkeypatch: Any) -> None:
    # count sends no device-side budget, so the inference margin that pads
    # every waiting call must not stretch a timeout the caller gave count.
    driver = _driver(fake_daemon)
    seen: list[float | None] = []
    real_call = driver._transport.call

    def spy(method: str, params: Any = None, *, timeout: float | None = None) -> Any:
        seen.append(timeout)
        return real_call(method, params, timeout=timeout)

    monkeypatch.setattr(driver._transport, "call", spy)
    driver.get_by_text("Save").count(timeout=1)
    assert seen and seen[-1] == 1


def test_locator_handles_share_no_spec_state(fake_daemon: Any) -> None:
    driver = _driver(fake_daemon)
    scope = driver.get_by_text("Dialog")
    loc = driver.get_by_text("Save").within(scope)
    loc._spec["within"]["text"] = "changed"
    assert scope._spec["text"] == "Dialog"
