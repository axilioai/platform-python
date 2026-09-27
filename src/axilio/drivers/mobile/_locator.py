"""Locator: a Playwright-style lazy handle over the DCP Locator action tier.

A `Locator` describes a target; it sends nothing until an action or query is
called, so it always resolves against whatever is on screen at that moment
(unlike the old `find()`, which froze a bounding box that could be stale by
the time you acted on it). Resolution, auto-wait, and the action itself
happen together on the device in one round trip.
"""

from __future__ import annotations

import copy
from collections.abc import Sequence
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Literal

from ._envelope import (
    METHOD_LOCATOR_BOUNDING_BOX,
    METHOD_LOCATOR_COUNT,
    METHOD_LOCATOR_FILL,
    METHOD_LOCATOR_PRESS,
    METHOD_LOCATOR_TAP,
    METHOD_LOCATOR_TEXT,
    METHOD_LOCATOR_WAIT_FOR,
)
from .types import BBox

if TYPE_CHECKING:
    from ._driver import MobileDriver

# Same alias as _driver.OcrEngine: an engine tier, e.g. "free" / "premium".
OcrEngine = Any

Strategy = Literal["auto", "vision", "accessibility"]
WaitState = Literal["visible", "hidden", "enabled"]


def _build_spec(
    *,
    query: str | None = None,
    text: str | None = None,
    role: str | None = None,
    name: str | None = None,
    id: str | None = None,  # noqa: A002 (mirrors the wire field name)
    states: Sequence[str] | None = None,
    exact: bool | None = None,
    android_class_name: str | None = None,
) -> dict[str, Any]:
    """The wire `Locator` object for these fields; omitted where unset."""
    spec: dict[str, Any] = {}
    if role is not None:
        spec["role"] = role
    if name is not None:
        spec["name"] = name
    if text is not None:
        spec["text"] = text
    if exact is not None:
        spec["exact"] = exact
    if id is not None:
        spec["id"] = id
    if states is not None:
        spec["states"] = list(states)
    if query is not None:
        spec["query"] = query
    if android_class_name is not None:
        spec["platform"] = {"android": {"className": android_class_name}}
    return spec


@dataclass(frozen=True)
class LocatorResult:
    """The outcome of one Locator action or query.

    `resolved_by` and `bounds` describe the resolved target and are `None`
    when the method doesn't resolve one (`press()` without a locator,
    `wait_for(state="hidden")`). `model_name` is set only when
    `resolved_by == "vlm"`.
    """

    resolved_by: Literal["a11y", "ocr", "vlm"] | None
    bounds: BBox | None
    took_ms: int
    model_name: str | None = None

    @classmethod
    def _from_wire(cls, wire: dict[str, Any]) -> LocatorResult:
        bounds = wire.get("bounds")
        return cls(
            resolved_by=wire.get("resolvedBy"),
            bounds=(
                BBox(
                    x=int(bounds["x"]),
                    y=int(bounds["y"]),
                    width=int(bounds["width"]),
                    height=int(bounds["height"]),
                )
                if bounds
                else None
            ),
            took_ms=int(wire.get("tookMs", 0)),
            model_name=wire.get("modelName"),
        )


class Locator:
    """A lazy, immutable description of a target on screen.

    Build one from `MobileDriver.locator()` / `get_by_text()` / `get_by_role()`
    / `get_by_id()`, refine it with `nth()` / `first()` / `within()` / `has()`
    / `filter()` (each returns a new `Locator`; the receiver is unchanged),
    then call an action or query; nothing is sent over the wire before that.

    `role` / `name` / `id` / `states` / the `platform` selectors need the
    accessibility tree: on phones that don't expose one (all of them today),
    they fail with `StrategyUnavailableError` regardless of `strategy`.
    `text` resolves by OCR when there's no tree.
    `query` (a natural-language description) is ranked by a model:
    over the accessibility tree when there is one, otherwise read straight
    off the screen by the VLM.
    """

    def __init__(self, driver: MobileDriver, spec: dict[str, Any]) -> None:
        self._driver = driver
        # A private deep copy: no two handles share a nested within/has spec,
        # so no handle can change another's target.
        self._spec = copy.deepcopy(spec)

    # --- refinement: each returns a new Locator ---------------------------

    def nth(self, n: int) -> Locator:
        """The `n`th match in reading order, zero-based."""
        return self._refine(nth=n)

    def first(self) -> Locator:
        """The first match in reading order; shorthand for `nth(0)`."""
        return self.nth(0)

    def within(self, other: Locator) -> Locator:
        """Refine to a match that is inside `other`.

        Refinements only ever narrow: calling `within` again scopes the new
        ancestor inside the earlier one rather than dropping it.
        """
        return self._refine(within=_chain_scope(other._spec, self._spec.get("within"), "within"))

    def has(self, other: Locator) -> Locator:
        """Refine to a match that contains `other`.

        Calling `has` again chains the new descendant onto the earlier one
        rather than dropping it.
        """
        return self._refine(has=_chain_scope(other._spec, self._spec.get("has"), "has"))

    def filter(self, *, query: str) -> Locator:
        """Add a semantic query on top of this locator's literal fields.

        The literal parts (role/name/text/id/…) still filter the
        candidates; the model then ranks the survivors by `query`. Useful
        for picking one of several matches ("the cheapest one") without
        giving up the cheap literal match. A second `filter` appends to the
        first query rather than replacing it.
        """
        existing = self._spec.get("query")
        return self._refine(query=f"{existing}, {query}" if existing else query)

    def _refine(self, **overrides: Any) -> Locator:
        return Locator(self._driver, {**self._spec, **overrides})

    # --- actions ------------------------------------------------------------

    def tap(
        self,
        *,
        timeout: float | None = None,
        strategy: Strategy | None = None,
        model: str | None = None,
        ocr_engine: OcrEngine | None = None,
    ) -> LocatorResult:
        """Resolve, auto-wait until actionable, then tap the target's centre."""
        wire = self._driver._locator_call(
            METHOD_LOCATOR_TAP,
            self._spec,
            timeout=timeout,
            strategy=strategy,
            model=model,
            ocr_engine=ocr_engine,
        )
        return LocatorResult._from_wire(wire or {})

    def fill(
        self,
        text: str,
        *,
        timeout: float | None = None,
        strategy: Strategy | None = None,
        model: str | None = None,
        ocr_engine: OcrEngine | None = None,
    ) -> LocatorResult:
        """Resolve and wait as `tap()`, focus the target, then type `text`."""
        wire = self._driver._locator_call(
            METHOD_LOCATOR_FILL,
            self._spec,
            extra={"text": text},
            timeout=timeout,
            strategy=strategy,
            model=model,
            ocr_engine=ocr_engine,
        )
        return LocatorResult._from_wire(wire or {})

    def press(
        self,
        key: str,
        *,
        timeout: float | None = None,
        strategy: Strategy | None = None,
        model: str | None = None,
        ocr_engine: OcrEngine | None = None,
    ) -> LocatorResult:
        """Resolve, wait, and focus the target, then press a named key."""
        wire = self._driver._locator_call(
            METHOD_LOCATOR_PRESS,
            self._spec,
            extra={"key": key},
            timeout=timeout,
            strategy=strategy,
            model=model,
            ocr_engine=ocr_engine,
        )
        return LocatorResult._from_wire(wire or {})

    def wait_for(
        self,
        *,
        state: WaitState = "visible",
        timeout: float | None = None,
        strategy: Strategy | None = None,
        model: str | None = None,
        ocr_engine: OcrEngine | None = None,
    ) -> LocatorResult | None:
        """Block on the device until the locator reaches `state`.

        Returns the resolved target's `LocatorResult`, or `None` for
        `state="hidden"` (there is nothing to describe once it's gone).
        """
        extra = {"state": state} if state != "visible" else None
        wire = self._driver._locator_call(
            METHOD_LOCATOR_WAIT_FOR,
            self._spec,
            extra=extra,
            timeout=timeout,
            strategy=strategy,
            model=model,
            ocr_engine=ocr_engine,
        )
        if state == "hidden":
            return None
        return LocatorResult._from_wire(wire or {})

    # --- queries --------------------------------------------------------

    def bounding_box(
        self,
        *,
        timeout: float | None = None,
        strategy: Strategy | None = None,
        model: str | None = None,
        ocr_engine: OcrEngine | None = None,
    ) -> LocatorResult:
        """Wait until the locator resolves, then return its bounds (`.bounds`)."""
        wire = self._driver._locator_call(
            METHOD_LOCATOR_BOUNDING_BOX,
            self._spec,
            timeout=timeout,
            strategy=strategy,
            model=model,
            ocr_engine=ocr_engine,
        )
        return LocatorResult._from_wire(wire or {})

    def text(
        self,
        *,
        timeout: float | None = None,
        strategy: Strategy | None = None,
        model: str | None = None,
        ocr_engine: OcrEngine | None = None,
    ) -> str:
        """Wait until the locator resolves, then return its text."""
        wire = self._driver._locator_call(
            METHOD_LOCATOR_TEXT,
            self._spec,
            timeout=timeout,
            strategy=strategy,
            model=model,
            ocr_engine=ocr_engine,
        )
        return str((wire or {}).get("text", ""))

    def count(
        self,
        *,
        timeout: float | None = None,
        strategy: Strategy | None = None,
        model: str | None = None,
        ocr_engine: OcrEngine | None = None,
    ) -> int:
        """Count the targets matching this locator on the current screen.

        Zero included; never waits (there is no `timeoutMs` on the wire for
        this one; `timeout` here only bounds the SDK's own call).
        """
        wire = self._driver._locator_call(
            METHOD_LOCATOR_COUNT,
            self._spec,
            send_timeout_ms=False,
            timeout=timeout,
            strategy=strategy,
            model=model,
            ocr_engine=ocr_engine,
        )
        return int((wire or {}).get("count", 0))


def _chain_scope(scope: dict[str, Any], prev: dict[str, Any] | None, key: str) -> dict[str, Any]:
    """Attach `prev` at the innermost end of `scope`'s `key` chain.

    Keeps an earlier within/has scope instead of replacing it, so chaining
    refinements never widens a locator. Neither input is mutated.
    """
    if prev is None:
        return scope
    inner = scope.get(key)
    return {**scope, key: prev if inner is None else _chain_scope(inner, prev, key)}
