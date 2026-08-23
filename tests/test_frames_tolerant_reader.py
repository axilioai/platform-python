"""Tolerant-reader behavior of the unified frame envelope (AXI-1851).

The contract: unknown ``kind`` surfaces as an explicit UnknownFrame carrying
the raw JSON (never an error, never a silent drop); unknown fields inside
known kinds are ignored; unknown ``span_type``/``log_type`` values parse; a
message may be one frame object or an array. Live WS and the REST archive
share this envelope, so these tests pin the one deserializer both use.

The generated union is deliberately pinned as *strict* below: if a regen makes
it tolerant, the hand-written shim in ``axilio.platform._frames`` can shrink.
"""

from __future__ import annotations

import pydantic
import pytest

from axilio.core.pydantic_utilities import parse_obj_as
from axilio.platform import UnknownFrame, parse_frame, parse_frames
from axilio.types.run_session_frames_response_frames_item import (
    RunSessionFramesResponseFramesItem,
    RunSessionFramesResponseFramesItem_Log,
    RunSessionFramesResponseFramesItem_Span,
)

_SPAN = {
    "kind": "span",
    "name": "Screen.observe",
    "phase": "end",
    "span_id": "a" * 16,
    "span_type": "sdk_call",
    "start_time_unix_nano": 1,
    "end_time_unix_nano": 2,
    "status": {"code": "ok", "message": ""},
    "trace_id": "b" * 32,
}

_LOG = {
    "kind": "log",
    "body": "hello",
    "log_type": "agent",
    "severity": "info",
    "time_unix_nano": 3,
    "trace_id": "b" * 32,
}


def test_unknown_kind_surfaces_as_unknown_frame_with_raw_json() -> None:
    raw = {"kind": "telemetry_v2", "payload": {"nested": True}}
    frames = parse_frames([_SPAN, raw, _LOG])
    assert len(frames) == 3  # nothing dropped
    assert isinstance(frames[0], RunSessionFramesResponseFramesItem_Span)
    assert isinstance(frames[2], RunSessionFramesResponseFramesItem_Log)
    unknown = frames[1]
    assert isinstance(unknown, UnknownFrame)
    assert unknown.kind == "telemetry_v2"
    assert unknown.raw == raw


def test_unknown_field_in_known_kind_is_ignored() -> None:
    frame = parse_frame({**_LOG, "brand_new_field": {"x": 1}})
    assert isinstance(frame, RunSessionFramesResponseFramesItem_Log)
    assert frame.body == "hello"


def test_unknown_span_type_and_log_type_values_parse() -> None:
    span = parse_frame({**_SPAN, "span_type": "quantum_leap"})
    log = parse_frame({**_LOG, "log_type": "quantum_log"})
    assert isinstance(span, RunSessionFramesResponseFramesItem_Span)
    assert span.span_type == "quantum_leap"
    assert isinstance(log, RunSessionFramesResponseFramesItem_Log)
    assert log.log_type == "quantum_log"


def test_single_object_message_is_accepted() -> None:
    frames = parse_frames(_SPAN)
    assert len(frames) == 1
    assert isinstance(frames[0], RunSessionFramesResponseFramesItem_Span)


def test_missing_kind_becomes_unknown_frame() -> None:
    frame = parse_frame({"body": "no kind at all"})
    assert isinstance(frame, UnknownFrame)
    assert frame.kind == ""


def test_generated_union_is_still_strict_on_unknown_kind() -> None:
    # Documents WHY the shim exists. If a regen makes the generated union
    # tolerant (an explicit unknown variant), this fails: revisit _frames.py.
    with pytest.raises(pydantic.ValidationError):
        parse_obj_as(RunSessionFramesResponseFramesItem, {"kind": "telemetry_v2"})  # type: ignore[arg-type]


def test_generated_model_accepts_start_phase_span_without_end_or_status() -> None:
    # Spec 0.82.0 made end_time_unix_nano and status Optional to match the
    # live wire's start-phase frames. If a regen re-tightens them, the shim's
    # canonicalization comment in _frames.py is wrong again: revisit both.
    start = {k: v for k, v in _SPAN.items() if k not in ("end_time_unix_nano", "status")}
    start["phase"] = "start"
    parsed: RunSessionFramesResponseFramesItem = parse_obj_as(
        RunSessionFramesResponseFramesItem, start  # type: ignore[arg-type]
    )
    assert isinstance(parsed, RunSessionFramesResponseFramesItem_Span)
    assert parsed.end_time_unix_nano is None
    assert parsed.status is None


def test_parse_frame_canonicalizes_in_flight_span() -> None:
    # The shim presents absence as the in-flight sentinels downstream code
    # keys off: end 0, status code "" — never None.
    start = {k: v for k, v in _SPAN.items() if k not in ("end_time_unix_nano", "status")}
    start["phase"] = "start"
    frame = parse_frame(start)
    assert isinstance(frame, RunSessionFramesResponseFramesItem_Span)
    assert frame.end_time_unix_nano == 0
    assert frame.status is not None and frame.status.code == ""
