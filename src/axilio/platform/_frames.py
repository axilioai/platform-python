"""Tolerant deserializer for the unified frame envelope.

The frame contract (sessions_list_frames and the live telemetry WebSocket —
"live and archive differ only in cardinality") mandates a tolerant reader:
unknown ``kind`` values surface as an explicit UnknownFrame carrying the raw
JSON, unknown fields inside known kinds are ignored, unknown
``span_type``/``log_type`` values parse without error, and a message may carry
one frame object or an array of them.

Fern generates the known span/log models. A post-generation patch adds a
raw-preserving unknown variant to the REST response union; this module maps
that generated transport variant onto the stable public ``UnknownFrame`` used
by both archive and live helpers. It also keeps the live parser independent of
the REST response wrapper.

Hand-written and preserved across ``fern generate`` via ``src/axilio/.fernignore``
(under ``platform/``).
"""

from __future__ import annotations

import typing

from ..core.pydantic_utilities import UniversalBaseModel, parse_obj_as
from ..types.run_session_frames_response_frames_item import (
    RunSessionFramesResponseFramesItem,
    RunSessionFramesResponseFramesItem_Log,
    RunSessionFramesResponseFramesItem_Span,
    RunSessionFramesResponseFramesItem_Unknown,
)

# The discriminant values the generated union knows. A frame whose kind is not
# here becomes an UnknownFrame; everything else goes through the generated
# parser so field handling stays identical to the REST response types.
_KNOWN_KINDS = frozenset({"log", "span"})


class UnknownFrame(UniversalBaseModel):
    """A frame whose ``kind`` this SDK version does not know.

    Carries the frame verbatim so callers can render it generically or log it;
    it must never be dropped and never raise.
    """

    kind: str
    raw: dict[str, typing.Any]


Frame = (
    RunSessionFramesResponseFramesItem_Span | RunSessionFramesResponseFramesItem_Log | UnknownFrame
)


def parse_frame(obj: dict[str, typing.Any]) -> Frame:
    """Parse one frame object, tolerantly."""
    kind = obj.get("kind")
    if isinstance(kind, str) and kind and kind not in _KNOWN_KINDS:
        return UnknownFrame(kind=kind, raw=obj)
    if not isinstance(kind, str) or not kind:
        # Unknown future discriminants are additive; malformed envelopes are
        # not. Delegate to the generated union to raise its ValidationError.
        return parse_obj_as(RunSessionFramesResponseFramesItem, obj)  # type: ignore[arg-type]
    # Live-leg canonicalization: a start-phase frame describes an OPEN span,
    # so the wire omits end_time_unix_nano and status entirely (the archive
    # always has both — it returns completed spans only). Since spec 0.82.0
    # the generated model accepts the absence (both fields are Optional);
    # we still canonicalize to the falsy shapes consumers key off for
    # "in flight" — end 0, status code "" — so downstream code never
    # branches on None.
    if kind == "span" and ("end_time_unix_nano" not in obj or "status" not in obj):
        obj = dict(obj)
        obj.setdefault("end_time_unix_nano", 0)
        obj.setdefault("status", {"code": "", "message": ""})
    return parse_obj_as(RunSessionFramesResponseFramesItem, obj)  # type: ignore[arg-type]


def response_frame(frame: RunSessionFramesResponseFramesItem) -> Frame:
    """Map a generated REST union member onto the public helper surface."""
    if isinstance(frame, RunSessionFramesResponseFramesItem_Unknown):
        return UnknownFrame(kind=frame.kind, raw=frame.raw)
    return typing.cast(Frame, frame)


def parse_frames(
    payload: dict[str, typing.Any] | list[dict[str, typing.Any]],
) -> list[Frame]:
    """Parse a frame message: a single frame object or an array of them."""
    if isinstance(payload, list):
        return [parse_frame(obj) for obj in payload]
    return [parse_frame(payload)]
