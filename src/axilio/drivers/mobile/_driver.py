"""MobileDriver — the chainable selector driver."""

from __future__ import annotations

import base64
import time
from collections.abc import Callable
from datetime import datetime, timezone
from typing import Any

from . import _envelope
from ._errors import ElementNotFoundError, InternalError, TimeoutError
from ._transport import SandboxTransport, Transport
from .keys import Key
from .types import BBox, Coords, Element, IconBox, Screen

OcrEngine = Any


def _datetime_from_epoch_ms(epoch_ms: int) -> datetime:
    return datetime.fromtimestamp(epoch_ms / 1000, tz=timezone.utc)


class MobileDriver:
    """Drives a paired device through a `Transport`."""

    def __init__(self, transport: Transport) -> None:
        self._transport = transport

    @classmethod
    def connect(cls, *, socket_path: str | None = None) -> MobileDriver:
        """Connect to the sandbox's pre-allocated device over the daemon socket."""
        return cls(SandboxTransport(socket_path=socket_path))

    def observe(self, *, ocr_engine: OcrEngine = "free") -> Screen:
        """Capture the current frame and return a typed `Screen`."""
        result = self._transport.call(_envelope.METHOD_SCREEN_OBSERVE, {"ocr_engine": ocr_engine})
        return self._screen_from_wire(result or {})

    def find_text(
        self, text: str, *, exact: bool = False, ocr_engine: OcrEngine = "free"
    ) -> Element | None:
        """First OCR element matching `text` (one `observe()` per call)."""
        return self.observe(ocr_engine=ocr_engine).find_text(text, exact=exact)

    def find_all_text(
        self,
        *,
        contains: str | None = None,
        pattern: str | None = None,
        ocr_engine: OcrEngine = "free",
    ) -> list[Element]:
        """Every OCR element matching the criteria."""
        return self.observe(ocr_engine=ocr_engine).find_all_text(contains=contains, pattern=pattern)

    def find(
        self,
        *,
        query: str,
        timeout: float = 10.0,
        ocr_engine: OcrEngine = "free",
        model: str | None = None,
    ) -> Element:
        """VLM-backed semantic find via Argus (through the on-device agent)."""
        args: dict[str, Any] = {"query": query, "ocr_engine": ocr_engine}
        if model is not None:
            args["model"] = model
        result = self._transport.call(
            _envelope.METHOD_SCREEN_FIND,
            args,
            timeout=timeout,
        )
        found = (result or {}).get("found")
        if not found:
            raise ElementNotFoundError(f"no element on screen matched query: {query!r}")
        return self._element_from_found(found)

    def wait_for_text(
        self,
        text: str,
        *,
        timeout: float = 10.0,
        poll_ms: int = 300,
        exact: bool = False,
        ocr_engine: OcrEngine = "free",
    ) -> Element:
        """Poll `find_text` until the target appears or `timeout` elapses."""

        def probe() -> Element | None:
            return self.find_text(text, exact=exact, ocr_engine=ocr_engine)

        el = self._poll(probe, timeout=timeout, poll_ms=poll_ms)
        if el is None:
            raise TimeoutError(f"text not found within {timeout}s: {text!r}")
        return el

    def wait_until_gone(
        self,
        text: str,
        *,
        timeout: float = 10.0,
        poll_ms: int = 300,
        exact: bool = False,
        ocr_engine: OcrEngine = "free",
    ) -> None:
        """Poll until `text` disappears or `timeout` elapses."""

        def probe() -> bool | None:
            gone = self.find_text(text, exact=exact, ocr_engine=ocr_engine) is None
            return True if gone else None

        if self._poll(probe, timeout=timeout, poll_ms=poll_ms) is None:
            raise TimeoutError(f"text still present after {timeout}s: {text!r}")

    def wait_for(
        self,
        predicate: Callable[[Screen], object],
        *,
        timeout: float = 10.0,
        poll_ms: int = 300,
    ) -> Screen:
        """Poll `observe()` until `predicate(screen)` is truthy."""
        deadline = time.monotonic() + timeout
        while True:
            screen = self.observe()
            if predicate(screen):
                return screen
            if time.monotonic() >= deadline:
                raise TimeoutError(f"predicate not satisfied within {timeout}s")
            time.sleep(poll_ms / 1000)

    def tap(self, coords: Coords) -> None:
        """Tap once at `coords`."""
        self._tap_xy(int(coords["x"]), int(coords["y"]))

    def long_press(self, coords: Coords, *, duration_ms: int = 800) -> None:
        """Press-and-hold at `coords` for `duration_ms`."""
        self._long_press_xy(int(coords["x"]), int(coords["y"]), duration_ms)

    def swipe(self, start: Coords, end: Coords, *, duration_ms: int = 300) -> None:
        """Swipe from `start` to `end` over `duration_ms`."""
        self._swipe_xy(int(start["x"]), int(start["y"]), int(end["x"]), int(end["y"]), duration_ms)

    def type_text(self, text: str) -> None:
        """Type a string of US-layout-typable text."""
        self._type_text(text)

    def key_press(self, key: int) -> None:
        """Emit a single HID consumer-page key press."""
        self._transport.call(_envelope.METHOD_INPUT_KEY_PRESS, {"usage": int(key) & 0xFFFF})

    def screenshot(self) -> bytes:
        """Capture the current frame as PNG-encoded bytes."""
        result = self._transport.call(_envelope.METHOD_SCREEN_SCREENSHOT)
        if not result:
            raise InternalError("screenshot returned no result")
        encoded = result.get("png_base64")
        if not isinstance(encoded, str):
            raise InternalError(f"screenshot result missing png_base64: {result!r}")
        try:
            return base64.b64decode(encoded)
        except (ValueError, TypeError) as e:
            raise InternalError(f"screenshot base64 decode failed: {e}") from e

    def close(self) -> None:
        """Release the underlying transport. The next call reconnects."""
        self._transport.close()

    def __enter__(self) -> MobileDriver:
        return self

    def __exit__(self, *_: object) -> None:
        self.close()

    def _tap_xy(self, x: int, y: int) -> None:
        self._transport.call(_envelope.METHOD_INPUT_TAP, {"x": x, "y": y})

    def _long_press_xy(self, x: int, y: int, duration_ms: int) -> None:
        self._transport.call(
            _envelope.METHOD_INPUT_LONG_PRESS, {"x": x, "y": y, "duration_ms": int(duration_ms)}
        )

    def _swipe_xy(self, x1: int, y1: int, x2: int, y2: int, duration_ms: int) -> None:
        self._transport.call(
            _envelope.METHOD_INPUT_SWIPE,
            {"x1": x1, "y1": y1, "x2": x2, "y2": y2, "duration_ms": int(duration_ms)},
        )

    def _type_text(self, text: str) -> None:
        self._transport.call(_envelope.METHOD_INPUT_TYPE_TEXT, {"text": str(text)})

    def _poll(
        self,
        probe: Callable[[], Any],
        *,
        timeout: float,
        poll_ms: int,
    ) -> Any:
        deadline = time.monotonic() + timeout
        while True:
            value = probe()
            if value:
                return value
            if time.monotonic() >= deadline:
                return None
            time.sleep(poll_ms / 1000)

    @staticmethod
    def _bbox(wire: dict[str, Any]) -> BBox:
        return BBox(
            x=int(wire["x"]),
            y=int(wire["y"]),
            width=int(wire["width"]),
            height=int(wire["height"]),
        )

    @staticmethod
    def _center(bbox: BBox) -> Coords:
        return Coords(x=bbox["x"] + bbox["width"] // 2, y=bbox["y"] + bbox["height"] // 2)

    def _element_from_text(self, wire: dict[str, Any]) -> Element:
        bbox = self._bbox(wire["bbox"])
        return Element(
            bbox=bbox,
            center=self._center(bbox),
            confidence=float(wire.get("confidence", 0.0)),
            text=wire.get("text"),
            source="ocr",
            _driver=self,
        )

    def _element_from_found(self, wire: dict[str, Any]) -> Element:
        bbox = self._bbox(wire["bbox"])
        text = wire.get("text") or None
        return Element(
            bbox=bbox,
            center=self._center(bbox),
            confidence=float(wire.get("confidence", 0.0)),
            text=text,
            source="ocr" if text else "vlm",
            _driver=self,
        )

    def _icon_from_wire(self, wire: dict[str, Any]) -> IconBox:
        bbox = self._bbox(wire["bbox"])
        return IconBox(
            bbox=bbox,
            center=self._center(bbox),
            confidence=float(wire.get("confidence", 0.0)),
        )

    def _screen_from_wire(self, wire: dict[str, Any]) -> Screen:
        return Screen(
            texts=[self._element_from_text(text_wire) for text_wire in wire.get("texts") or []],
            icons=[self._icon_from_wire(icon_wire) for icon_wire in wire.get("icons") or []],
            hash=str(wire.get("hash", "")),
            width=int(wire.get("width", 0)),
            height=int(wire.get("height", 0)),
            captured_at=_datetime_from_epoch_ms(int(wire.get("captured_at", 0))),
        )


__all__ = ["MobileDriver", "Key"]
