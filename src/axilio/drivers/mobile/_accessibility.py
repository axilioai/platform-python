"""The phone's accessibility tree over the DCP `Accessibility` domain.

`driver.accessibility` reads the raw tree (`snapshot()`, `query()`,
`partial()`, `children()`) and turns it on or off mid-session (`enable()`,
`disable()`). Locators don't need any of this: they use the tree on their
own whenever the session has one.

The domain exists only on sessions whose handshake advertises it; on any
other session every method here raises `UnknownOpError`. The types are
snake_case over the camelCase wire.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import TYPE_CHECKING, Any, Literal

from . import _envelope
from .types import BBox

if TYPE_CHECKING:
    from ._locator import Locator
    from ._transport import Transport

WindowType = Literal["application", "inputMethod", "system", "overlay", "other"]


def _bbox(wire: dict[str, Any]) -> BBox:
    return BBox(
        x=int(wire.get("x", 0)),
        y=int(wire.get("y", 0)),
        width=int(wire.get("width", 0)),
        height=int(wire.get("height", 0)),
    )


@dataclass(frozen=True)
class AXValue:
    """A typed value, as CDP shapes it: `type` is the CDP AXValueType (e.g.
    "role", "computedString", "boolean") and `value` a str, bool or number."""

    type: str
    value: Any = None

    @classmethod
    def _from_wire(cls, wire: dict[str, Any]) -> AXValue:
        return cls(type=str(wire.get("type", "")), value=wire.get("value"))

    @classmethod
    def _maybe(cls, wire: dict[str, Any] | None) -> AXValue | None:
        return cls._from_wire(wire) if wire else None


@dataclass(frozen=True)
class AXProperty:
    """One named node property, e.g. `checked`, `focusable`, `editable`."""

    name: str
    value: AXValue


@dataclass(frozen=True)
class AXAndroidNode:
    """The node's native Android fields. Not portable."""

    class_name: str | None = None
    view_id_resource_name: str | None = None
    package_name: str | None = None
    text: str | None = None
    content_description: str | None = None
    hint_text: str | None = None

    @classmethod
    def _from_wire(cls, wire: dict[str, Any]) -> AXAndroidNode:
        return cls(
            class_name=wire.get("className"),
            view_id_resource_name=wire.get("viewIdResourceName"),
            package_name=wire.get("packageName"),
            text=wire.get("text"),
            content_description=wire.get("contentDescription"),
            hint_text=wire.get("hintText"),
        )


@dataclass(frozen=True)
class AXNode:
    """One node of the tree: CDP's AXNode plus `bounds`, `window_id`,
    `actions` and the native `android` fields.

    `node_id` is stable while the element lives, so it can pin a locator
    (`driver.locator(node_id=...)`) or seed `partial()` / `children()`.
    `bounds` are frame pixels, the same space `driver.tap()` addresses.
    """

    node_id: str
    ignored: bool
    role: AXValue
    child_ids: list[str]
    bounds: BBox
    window_id: str
    actions: list[str]
    name: AXValue | None = None
    description: AXValue | None = None
    value: AXValue | None = None
    properties: list[AXProperty] | None = None
    parent_id: str | None = None
    android: AXAndroidNode | None = None

    @classmethod
    def _from_wire(cls, wire: dict[str, Any]) -> AXNode:
        props = wire.get("properties")
        android = (wire.get("platform") or {}).get("android")
        return cls(
            node_id=str(wire.get("nodeId", "")),
            ignored=bool(wire.get("ignored", False)),
            role=AXValue._from_wire(wire.get("role") or {}),
            child_ids=[str(c) for c in wire.get("childIds") or []],
            bounds=_bbox(wire.get("bounds") or {}),
            window_id=str(wire.get("windowId", "")),
            actions=[str(a) for a in wire.get("actions") or []],
            name=AXValue._maybe(wire.get("name")),
            description=AXValue._maybe(wire.get("description")),
            value=AXValue._maybe(wire.get("value")),
            properties=(
                [
                    AXProperty(name=str(p.get("name", "")), value=AXValue._from_wire(p["value"]))
                    for p in props
                ]
                if props is not None
                else None
            ),
            parent_id=wire.get("parentId"),
            android=AXAndroidNode._from_wire(android) if android else None,
        )


@dataclass(frozen=True)
class AXWindow:
    """One window on screen. `app` is the owning package, when known."""

    window_id: str
    type: WindowType
    focused: bool
    bounds: BBox
    title: str | None = None
    app: str | None = None
    root_id: str | None = None

    @classmethod
    def _from_wire(cls, wire: dict[str, Any]) -> AXWindow:
        return cls(
            window_id=str(wire.get("windowId", "")),
            type=wire.get("type", "other"),
            focused=bool(wire.get("focused", False)),
            bounds=_bbox(wire.get("bounds") or {}),
            title=wire.get("title"),
            app=wire.get("app"),
            root_id=wire.get("rootId"),
        )


@dataclass(frozen=True)
class AXTree:
    """A snapshot of the tree: every node in document order, and the windows."""

    nodes: list[AXNode]
    windows: list[AXWindow]
    captured_at: datetime

    @classmethod
    def _from_wire(cls, wire: dict[str, Any]) -> AXTree:
        return cls(
            nodes=_nodes(wire),
            windows=[AXWindow._from_wire(w) for w in wire.get("windows") or []],
            captured_at=datetime.fromtimestamp(
                int(wire.get("capturedAt", 0)) / 1000, tz=timezone.utc
            ),
        )


@dataclass(frozen=True)
class AccessibilityState:
    """Whether the tree is on, and whether this session can turn it on and off."""

    enabled: bool
    toggleable: bool


def _nodes(wire: dict[str, Any] | None) -> list[AXNode]:
    return [AXNode._from_wire(n) for n in (wire or {}).get("nodes") or []]


class Accessibility:
    """`driver.accessibility`: the raw accessibility tree and its toggle.

    `enabled_at_allocation` is what allocate reported for this session (the
    `accessibility` flag on `client.session(...)`), or `None` when the
    driver didn't come from an allocation (a sandbox, or `connect_remote`
    without it). It doesn't follow a later
    `enable()` / `disable()`; `state()` asks the phone.

    While the tree is on, the accessibility service is visible to apps on
    the phone; `disable()` turns it fully off.
    """

    def __init__(self, transport: Transport, *, enabled_at_allocation: bool | None) -> None:
        self._transport = transport
        self.enabled_at_allocation = enabled_at_allocation

    def state(self) -> AccessibilityState:
        """Ask the phone whether the tree is on and whether it can be toggled."""
        wire = self._transport.call(_envelope.METHOD_ACCESSIBILITY_GET_STATE, {}) or {}
        return AccessibilityState(
            enabled=bool(wire.get("enabled", False)),
            toggleable=bool(wire.get("toggleable", False)),
        )

    def enable(self) -> None:
        """Turn the tree on. Returns once the phone confirms it is on."""
        self._transport.call(_envelope.METHOD_ACCESSIBILITY_ENABLE, {})

    def disable(self) -> None:
        """Turn the tree off. Returns once the phone confirms it is off;
        locators then resolve by vision."""
        self._transport.call(_envelope.METHOD_ACCESSIBILITY_DISABLE, {})

    def snapshot(
        self,
        *,
        interesting_only: bool = True,
        window_id: str | None = None,
        depth: int | None = None,
    ) -> AXTree:
        """The tree of every window (or just `window_id`), in document order.

        `interesting_only=False` keeps the layout-only nodes the default
        drops. `depth` limits how far below each window root to go (0 is the
        roots only). Raises `StrategyUnavailableError` while the tree is off
        and `TreeUnavailableError` when there is no app window to read (a
        system dialog is up).
        """
        params: dict[str, Any] = {}
        if not interesting_only:
            params["interestingOnly"] = False
        if window_id is not None:
            params["windowId"] = window_id
        if depth is not None:
            params["depth"] = depth
        wire = self._transport.call(_envelope.METHOD_ACCESSIBILITY_GET_FULL_AXTREE, params)
        return AXTree._from_wire(wire or {})

    def query(
        self,
        *,
        role: str | None = None,
        name: str | None = None,
        selector: Locator | None = None,
    ) -> list[AXNode]:
        """Every visible node matching `role`, the exact accessible `name`
        and `selector`, in reading order. Never waits.

        `selector` takes a locator's selector fields (`driver.get_by_text(...)`,
        `driver.locator(package_name=...)`, ...); its `query` isn't accepted
        here and its resolution options don't apply.
        """
        params: dict[str, Any] = {}
        if role is not None:
            params["role"] = role
        if name is not None:
            params["accessibleName"] = name
        if selector is not None:
            params["selector"] = selector._spec
        wire = self._transport.call(_envelope.METHOD_ACCESSIBILITY_QUERY_AXTREE, params)
        return _nodes(wire)

    def partial(self, node_id: str, *, fetch_relatives: bool = True) -> list[AXNode]:
        """One node, plus its ancestors, siblings and children unless
        `fetch_relatives=False`. Raises `StaleNodeError` once the node is gone."""
        params: dict[str, Any] = {"nodeId": node_id}
        if not fetch_relatives:
            params["fetchRelatives"] = False
        wire = self._transport.call(_envelope.METHOD_ACCESSIBILITY_GET_PARTIAL_AXTREE, params)
        return _nodes(wire)

    def children(self, node_id: str) -> list[AXNode]:
        """A node's children. Raises `StaleNodeError` once the node is gone."""
        wire = self._transport.call(
            _envelope.METHOD_ACCESSIBILITY_GET_CHILD_AXNODES, {"id": node_id}
        )
        return _nodes(wire)
