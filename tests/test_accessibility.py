"""driver.accessibility: the DCP Accessibility domain, wire shape and parsing."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

import pytest

from axilio.drivers.mobile import (
    AccessibilityState,
    AXAndroidNode,
    AXNode,
    AXProperty,
    AXTree,
    AXValue,
    AXWindow,
    MobileDriver,
    StaleNodeError,
    StrategyUnavailableError,
    TreeUnavailableError,
    UnknownOpError,
)
from axilio.drivers.mobile._transport import SandboxTransport

_NODE: dict[str, Any] = {
    "nodeId": "n2",
    "ignored": False,
    "role": {"type": "role", "value": "button"},
    "name": {"type": "computedString", "value": "Log in"},
    "properties": [{"name": "focusable", "value": {"type": "boolean", "value": True}}],
    "parentId": "n1",
    "childIds": [],
    "bounds": {"x": 10, "y": 20, "width": 300, "height": 80},
    "windowId": "w1",
    "actions": ["click", "longClick"],
    "platform": {
        "android": {
            "className": "android.widget.Button",
            "viewIdResourceName": "com.example.app:id/login",
            "packageName": "com.example.app",
            "text": "Log in",
        }
    },
}

_TREE: dict[str, Any] = {
    "nodes": [_NODE],
    "windows": [
        {
            "windowId": "w1",
            "type": "application",
            "focused": True,
            "bounds": {"x": 0, "y": 0, "width": 1080, "height": 2400},
            "app": "com.example.app",
            "rootId": "n1",
        }
    ],
    "capturedAt": 1780000000000,
}


def _driver(daemon: Any, **kwargs: Any) -> MobileDriver:
    return MobileDriver(SandboxTransport(socket_path=daemon.socket_path), **kwargs)


def _sent(daemon: Any, method: str) -> dict[str, Any]:
    return next(c for c in daemon.received if c["method"] == method)


def test_snapshot_sends_only_non_defaults_and_parses_tree(fake_daemon: Any) -> None:
    fake_daemon.responder = lambda cmd: {"id": cmd["id"], "result": _TREE}
    drv = _driver(fake_daemon)
    try:
        tree = drv.accessibility.snapshot()
        drv.accessibility.snapshot(interesting_only=False, window_id="w1", depth=0)
    finally:
        drv.close()

    calls = [c for c in fake_daemon.received if c["method"] == "Accessibility.getFullAXTree"]
    assert calls[0]["params"] == {}
    assert calls[1]["params"] == {"interestingOnly": False, "windowId": "w1", "depth": 0}

    assert tree == AXTree(
        nodes=[
            AXNode(
                node_id="n2",
                ignored=False,
                role=AXValue(type="role", value="button"),
                child_ids=[],
                bounds={"x": 10, "y": 20, "width": 300, "height": 80},
                window_id="w1",
                actions=["click", "longClick"],
                name=AXValue(type="computedString", value="Log in"),
                properties=[
                    AXProperty(name="focusable", value=AXValue(type="boolean", value=True))
                ],
                parent_id="n1",
                android=AXAndroidNode(
                    class_name="android.widget.Button",
                    view_id_resource_name="com.example.app:id/login",
                    package_name="com.example.app",
                    text="Log in",
                ),
            )
        ],
        windows=[
            AXWindow(
                window_id="w1",
                type="application",
                focused=True,
                bounds={"x": 0, "y": 0, "width": 1080, "height": 2400},
                app="com.example.app",
                root_id="n1",
            )
        ],
        captured_at=datetime.fromtimestamp(1780000000, tz=timezone.utc),
    )


def test_query_maps_name_to_accessible_name_and_takes_a_locator(fake_daemon: Any) -> None:
    fake_daemon.responder = lambda cmd: {"id": cmd["id"], "result": {"nodes": [_NODE]}}
    drv = _driver(fake_daemon)
    try:
        nodes = drv.accessibility.query(
            role="button",
            name="Log in",
            selector=drv.locator(package_name="com.example.app", model="ignored-here"),
        )
    finally:
        drv.close()

    assert _sent(fake_daemon, "Accessibility.queryAXTree")["params"] == {
        "role": "button",
        "accessibleName": "Log in",
        "selector": {"platform": {"android": {"packageName": "com.example.app"}}},
    }
    assert [n.node_id for n in nodes] == ["n2"]


def test_partial_and_children_wire_shape(fake_daemon: Any) -> None:
    fake_daemon.responder = lambda cmd: {"id": cmd["id"], "result": {"nodes": [_NODE]}}
    drv = _driver(fake_daemon)
    try:
        drv.accessibility.partial("n2")
        drv.accessibility.partial("n2", fetch_relatives=False)
        kids = drv.accessibility.children("n1")
    finally:
        drv.close()

    partials = [
        c["params"] for c in fake_daemon.received if c["method"] == "Accessibility.getPartialAXTree"
    ]
    assert partials == [{"nodeId": "n2"}, {"nodeId": "n2", "fetchRelatives": False}]
    assert _sent(fake_daemon, "Accessibility.getChildAXNodes")["params"] == {"id": "n1"}
    assert kids[0].node_id == "n2"


def test_state_enable_disable(fake_daemon: Any) -> None:
    def responder(cmd: dict[str, Any]) -> dict[str, Any]:
        if cmd["method"] == "Accessibility.getState":
            return {"id": cmd["id"], "result": {"enabled": True, "toggleable": True}}
        return {"id": cmd["id"], "result": {}}

    fake_daemon.responder = responder
    drv = _driver(fake_daemon)
    try:
        assert drv.accessibility.state() == AccessibilityState(enabled=True, toggleable=True)
        drv.accessibility.disable()
        drv.accessibility.enable()
    finally:
        drv.close()

    assert [c["method"] for c in fake_daemon.received] == [
        "Accessibility.getState",
        "Accessibility.disable",
        "Accessibility.enable",
    ]


def test_enabled_at_allocation_comes_from_the_driver() -> None:
    transport = SandboxTransport(socket_path="/tmp/unused.sock")
    assert MobileDriver(transport).accessibility.enabled_at_allocation is None
    drv = MobileDriver(transport, accessibility_at_allocation=True)
    assert drv.accessibility.enabled_at_allocation is True


@pytest.mark.parametrize(
    ("kind", "code", "exc"),
    [
        ("TreeUnavailable", -32011, TreeUnavailableError),
        ("StaleNode", -32012, StaleNodeError),
        ("StrategyUnavailable", -32010, StrategyUnavailableError),
        ("UnknownOp", -32601, UnknownOpError),
    ],
)
def test_accessibility_errors_map(
    fake_daemon: Any, kind: str, code: int, exc: type[Exception]
) -> None:
    fake_daemon.responder = lambda cmd: {
        "id": cmd["id"],
        "error": {"code": code, "message": kind, "data": {"kind": kind}},
    }
    drv = _driver(fake_daemon)
    try:
        with pytest.raises(exc):
            drv.accessibility.children("n1")
    finally:
        drv.close()
