"""Public types for the chainable selector surface."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import datetime
from typing import TYPE_CHECKING, Literal, TypedDict

if TYPE_CHECKING:
    from ._driver import MobileDriver


class Coords(TypedDict):
    """A point in frame-space pixels."""

    x: int
    y: int


class BBox(TypedDict):
    """An axis-aligned box in frame-space pixels (top-left origin)."""

    x: int
    y: int
    width: int
    height: int


def _matches(text: str | None, needle: str, *, exact: bool) -> bool:
    if text is None:
        return False
    if exact:
        return text == needle
    return needle.casefold() in text.casefold()


@dataclass(frozen=True)
class Element:
    """One located element — the universal selector return type; actions chain off it."""

    bbox: BBox
    center: Coords
    confidence: float
    text: str | None
    source: Literal["ocr", "vlm"]
    _driver: MobileDriver = field(repr=False, compare=False)

    def tap(self) -> None:
        """Tap at the element's center."""
        self._driver._tap_xy(self.center["x"], self.center["y"])

    def long_press(self, *, duration_ms: int = 800) -> None:
        """Press-and-hold at the element's center for `duration_ms`."""
        self._driver._long_press_xy(self.center["x"], self.center["y"], duration_ms)

    def type_into(self, text: str) -> None:
        """Tap the element, then type `text`."""
        self.tap()
        self._driver._type_text(text)

    def swipe_to(self, other: Element, *, duration_ms: int = 300) -> None:
        """Swipe from this element's center to `other`'s center."""
        self._driver._swipe_xy(
            self.center["x"],
            self.center["y"],
            other.center["x"],
            other.center["y"],
            duration_ms,
        )


@dataclass(frozen=True)
class IconBox:
    """One YOLO-detected icon (rectangle-only — the icon model has a single class)."""

    bbox: BBox
    center: Coords
    confidence: float


@dataclass(frozen=True)
class Screen:
    """An immutable snapshot of one observed frame."""

    texts: list[Element]
    icons: list[IconBox]
    hash: str
    width: int
    height: int
    captured_at: datetime

    def find_text(self, text: str, *, exact: bool = False) -> Element | None:
        """First OCR element whose text matches."""
        for el in self.texts:
            if _matches(el.text, text, exact=exact):
                return el
        return None

    def find_all_text(
        self,
        *,
        contains: str | None = None,
        pattern: str | None = None,
    ) -> list[Element]:
        """Every OCR element matching the criteria (`contains` and `pattern` are exclusive)."""
        if contains is not None and pattern is not None:
            raise ValueError("find_all_text: pass at most one of contains / pattern")
        if contains is not None:
            needle = contains.casefold()
            return [el for el in self.texts if el.text and needle in el.text.casefold()]
        if pattern is not None:
            regex = re.compile(pattern)
            return [el for el in self.texts if el.text and regex.search(el.text)]
        return list(self.texts)
