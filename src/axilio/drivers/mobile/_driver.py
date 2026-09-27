"""MobileDriver: drives a paired device over DCP."""

from __future__ import annotations

import base64
from datetime import datetime, timezone
from typing import Any

from . import _envelope
from ._errors import InternalError
from ._locator import Locator, LocatorResult, _build_spec
from ._transport import RemoteTransport, SandboxTransport, Transport
from .keys import Key
from .types import BBox, Coords, DeviceInfo, Element, HandshakeResult, IconBox, Screen

OcrEngine = Any

# Locator.* wire defaults/bounds (LocatorTimeoutMs in the contract): the
# server treats an omitted/zero timeoutMs as 5000, and rejects one over
# 60000. Mirrored here so the SDK can validate and size its own transport
# timeout without a round trip.
_DEFAULT_LOCATOR_TIMEOUT_MS = 5000
_MAX_LOCATOR_TIMEOUT_MS = 60000
# An inference already in flight when timeoutMs ends is allowed to finish
# (the contract's own words); this is slack on top of the device-side
# budget so the SDK's own socket read doesn't cut that off.
_LOCATOR_TRANSPORT_MARGIN_S = 15.0


def _datetime_from_epoch_ms(epoch_ms: int) -> datetime:
    return datetime.fromtimestamp(epoch_ms / 1000, tz=timezone.utc)


class MobileDriver:
    """Drives a paired device through a `Transport`.

    ``default_ocr_engine`` / ``default_model`` are session-wide defaults:
    `locator()` / `get_by_text()` each take ``ocr_engine=`` and ``model=``
    keyword-only, and use the driver default for any of those a locator
    doesn't set, so a script that wants the premium engine (or a specific
    VLM) everywhere sets it once instead of repeating the kwarg on every
    locator. A locator's own value always wins. When neither is set,
    ``ocr_engine`` falls back to ``"free"`` and ``model`` to the server-side
    default. `observe()`'s ``ocr_engine=`` and the driver-level `press()` are
    unaffected by this: `observe()` takes its own per-call ``ocr_engine=``,
    and `press()` (no locator) carries no resolution options at all.
    """

    def __init__(
        self,
        transport: Transport,
        *,
        default_ocr_engine: OcrEngine | None = None,
        default_model: str | None = None,
    ) -> None:
        self._transport = transport
        self._default_ocr_engine = default_ocr_engine
        self._default_model = default_model

    @classmethod
    def connect(
        cls,
        *,
        socket_path: str | None = None,
        default_ocr_engine: OcrEngine | None = None,
        default_model: str | None = None,
    ) -> MobileDriver:
        """Connect to the sandbox's pre-allocated device over the daemon socket."""
        return cls(
            SandboxTransport(socket_path=socket_path),
            default_ocr_engine=default_ocr_engine,
            default_model=default_model,
        )

    @classmethod
    def connect_remote(
        cls,
        control_url: str,
        *,
        open_timeout: float = 10.0,
        connect: Any | None = None,
        default_ocr_engine: OcrEngine | None = None,
        default_model: str | None = None,
    ) -> MobileDriver:
        """Connect to a remotely-allocated device over its DCP control URL.

        ``control_url`` is the value returned by ``client.devices.allocate(...)``
        — a ``wss://`` URL with the scoped, allocation-bound control token already
        embedded by the backend. Most callers should use ``client.session(...)``,
        which allocates, builds this driver, and releases the device on exit; use
        this directly when you want to manage the allocation lifecycle yourself.

        ``connect`` is an injectable WebSocket factory for tests; production opens
        a real socket lazily on the first call.
        """
        return cls(
            RemoteTransport(control_url, open_timeout=open_timeout, connect=connect),
            default_ocr_engine=default_ocr_engine,
            default_model=default_model,
        )

    def _resolve_engine(self, ocr_engine: OcrEngine | None) -> OcrEngine:
        """Per-call engine, else the driver default, else "free"."""
        if ocr_engine is not None:
            return ocr_engine
        if self._default_ocr_engine is not None:
            return self._default_ocr_engine
        return "free"

    def handshake(self) -> HandshakeResult:
        """Perform the DCP ``Protocol.handshake``.

        Returns the executor's advertised ``protocol_version``, device
        descriptor, ``domains`` and ``capabilities`` — call it once on connect
        to gate behavior on the returned capabilities instead of assuming the
        phone surface. This is not skew-tolerant: every executor implements the
        handshake, so any failure (including ``UnknownOp``) propagates.
        """
        result = self._transport.call(_envelope.METHOD_PROTOCOL_HANDSHAKE, {})
        return HandshakeResult._from_wire(result or {})

    def device_info(self) -> DeviceInfo:
        """Return the ``Device.info`` static descriptor.

        Like :meth:`handshake` this is not skew-tolerant: an executor that
        lacks it raises :class:`UnknownOpError`.
        """
        result = self._transport.call(_envelope.METHOD_DEVICE_INFO)
        return DeviceInfo._from_wire(result or {})

    def observe(self, *, ocr_engine: OcrEngine | None = None) -> Screen:
        """Capture the current frame and return a typed `Screen`."""
        result = self._transport.call(
            _envelope.METHOD_SCREEN_OBSERVE, {"ocr_engine": self._resolve_engine(ocr_engine)}
        )
        return self._screen_from_wire(result or {})

    # --- locators -----------------------------------------------------------
    #
    # A Locator is a lazy, immutable description of a target; building one
    # sends nothing. The wire round trip happens on an action or query
    # (`.tap()`, `.wait_for()`, `.count()`, ...), which resolves it against
    # the *current* screen, auto-waits until it's actionable, and (for
    # tap/fill/press) acts; all in one DCP call. See `Locator` for the
    # per-field resolution rules (`text` is OCR; `query` is model-ranked) and
    # for how `model` / `ocr_engine` on the locator flow into that call.
    #
    # Role/id/other accessibility-tree selectors, and `strategy`, aren't part
    # of the public surface yet: no phone exposes an accessibility tree
    # today, so they'd only ever fail with `StrategyUnavailableError`. They
    # arrive with accessibility support in a later release.

    def locator(
        self,
        *,
        query: str | None = None,
        text: str | None = None,
        exact: bool | None = None,
        model: str | None = None,
        ocr_engine: OcrEngine | None = None,
    ) -> Locator:
        """General locator constructor; every selector method is sugar for this.

        `model` / `ocr_engine` pick how *this* locator resolves; unset, each
        falls back to the driver's `default_model` / `default_ocr_engine`. A
        refinement (`nth()` / `first()` / `within()` / `has()` / `filter()`)
        keeps whatever this locator was built with.
        """
        spec = _build_spec(query=query, text=text, exact=exact)
        return Locator(self, spec, model=model, ocr_engine=ocr_engine)

    def get_by_text(
        self,
        text: str,
        *,
        exact: bool = False,
        model: str | None = None,
        ocr_engine: OcrEngine | None = None,
    ) -> Locator:
        """Locator matching visible text, resolved by OCR.

        See `locator()` for `model` / `ocr_engine`.
        """
        return self.locator(text=text, exact=exact, model=model, ocr_engine=ocr_engine)

    def press(self, key: str, *, timeout: float | None = None) -> LocatorResult:
        """Press a named key against whatever currently has focus.

        Equivalent to `Locator.press` without a locator; `resolved_by` /
        `bounds` are `None` on the result since nothing was resolved. Use
        `loc.press(key)` instead to focus a specific target first. Unlike a
        `Locator`'s actions, this takes no resolution options at all: there
        is nothing here for `model` / `ocr_engine` to apply to.
        """
        result = self._locator_call(
            _envelope.METHOD_LOCATOR_PRESS,
            None,
            extra={"key": key},
            timeout=timeout,
            resolve_options=False,
        )
        return LocatorResult._from_wire(result or {})

    def _locator_call(
        self,
        method: str,
        spec: dict[str, Any] | None,
        *,
        extra: dict[str, Any] | None = None,
        send_timeout_ms: bool = True,
        timeout: float | None,
        model: str | None = None,
        ocr_engine: OcrEngine | None = None,
        resolve_options: bool = True,
    ) -> dict[str, Any] | None:
        """Build and send one `Locator.*` command; shared by every Locator
        action/query and by `press()`.

        ``spec`` is the wire `locator` object, or `None` to omit it entirely
        (`press()` without a target). ``model`` / ``ocr_engine`` are the
        calling `Locator`'s own resolution options (each falls back to the
        matching driver default, then is omitted); ``resolve_options`` is
        `False` only for the driver-level `press()`, which has no locator and
        so sends neither regardless of driver defaults. ``timeout`` is in
        seconds and becomes `timeoutMs`, except for `Locator.count`
        (``send_timeout_ms=False``), which has no `timeoutMs` on the wire;
        ``timeout`` there only bounds the SDK's own call.

        `strategy` is never sent: with no accessibility tree on any phone
        today, vision is the only resolver, so there's nothing for it to pick
        between.
        """
        params: dict[str, Any] = {}
        if spec is not None:
            params["locator"] = spec
        if extra:
            params.update(extra)

        if resolve_options:
            model = model if model is not None else self._default_model
            if model is not None:
                params["model"] = model
            ocr_engine = ocr_engine if ocr_engine is not None else self._default_ocr_engine
            if ocr_engine is not None:
                params["ocrEngine"] = ocr_engine

        timeout_ms = _DEFAULT_LOCATOR_TIMEOUT_MS
        if timeout is not None:
            timeout_ms = round(timeout * 1000)
            if not 0 <= timeout_ms <= _MAX_LOCATOR_TIMEOUT_MS:
                raise ValueError(
                    f"timeout must be between 0 and {_MAX_LOCATOR_TIMEOUT_MS / 1000:g}s, "
                    f"got {timeout}s"
                )
            if send_timeout_ms:
                params["timeoutMs"] = timeout_ms

        # The margin covers an inference still running on the device when its
        # budget ends. Locator.count has no device-side budget, so a timeout
        # the caller gave it is the whole deadline.
        if send_timeout_ms or timeout is None:
            transport_timeout = timeout_ms / 1000 + _LOCATOR_TRANSPORT_MARGIN_S
        else:
            transport_timeout = timeout
        return self._transport.call(method, params, timeout=transport_timeout)

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

    def key_press(self, key: str) -> None:
        """Press a named key (see `Key`), e.g. `driver.key_press(Key.ENTER)`."""
        self._transport.call(_envelope.METHOD_KEYBOARD_KEY_PRESS, {"key": key})

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
        self._transport.call(_envelope.METHOD_TOUCH_TAP, {"x": x, "y": y})

    def _long_press_xy(self, x: int, y: int, duration_ms: int) -> None:
        self._transport.call(
            _envelope.METHOD_TOUCH_LONG_PRESS, {"x": x, "y": y, "duration_ms": int(duration_ms)}
        )

    def _swipe_xy(self, x1: int, y1: int, x2: int, y2: int, duration_ms: int) -> None:
        self._transport.call(
            _envelope.METHOD_TOUCH_SWIPE,
            {"x1": x1, "y1": y1, "x2": x2, "y2": y2, "duration_ms": int(duration_ms)},
        )

    def _type_text(self, text: str) -> None:
        self._transport.call(_envelope.METHOD_KEYBOARD_TYPE_TEXT, {"text": str(text)})

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
