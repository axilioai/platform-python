"""Tolerant-reader behavior of the unified frame envelope (AXI-1851).

The contract: unknown ``kind`` surfaces as an explicit UnknownFrame carrying
the raw JSON (never an error, never a silent drop); unknown fields inside
known kinds are ignored; unknown ``span_type``/``log_type`` values parse; a
message may be one frame object or an array. Live WS and the REST archive
share this envelope, so these tests pin the one deserializer both use.

The generated union is patched after every Fern regeneration so the archive
path has the same unknown-kind tolerance as the live helper.
"""

from __future__ import annotations

import typing

import pydantic
import pytest

from axilio.core.pydantic_utilities import parse_obj_as
from axilio.platform import UnknownFrame, parse_frame, parse_frames
from axilio.types.run_session_frames_response import RunSessionFramesResponse
from axilio.types.run_session_frames_response_frames_item import (
    RunSessionFramesResponseFramesItem,
    RunSessionFramesResponseFramesItem_Log,
    RunSessionFramesResponseFramesItem_Span,
    RunSessionFramesResponseFramesItem_Unknown,
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


@pytest.mark.parametrize("kind", [None, 3, ""])
def test_malformed_kind_is_rejected(kind: object) -> None:
    payload: dict[str, typing.Any] = {"body": "bad envelope"}
    if kind is not None:
        payload["kind"] = kind
    with pytest.raises(pydantic.ValidationError):
        parse_frame(payload)


def test_generated_union_preserves_unknown_kind_with_raw_json() -> None:
    raw = {"kind": "telemetry_v2", "payload": {"nested": True}}
    parsed: RunSessionFramesResponseFramesItem = parse_obj_as(
        RunSessionFramesResponseFramesItem, raw  # type: ignore[arg-type]
    )
    assert isinstance(parsed, RunSessionFramesResponseFramesItem_Unknown)
    assert parsed.kind == "telemetry_v2"
    assert parsed.raw == raw


def test_generated_unknown_kind_preserves_field_named_dict() -> None:
    raw = {"kind": "telemetry_v2", "dict": {"future": True}}
    parsed: RunSessionFramesResponseFramesItem = parse_obj_as(
        RunSessionFramesResponseFramesItem, raw  # type: ignore[arg-type]
    )

    assert isinstance(parsed, RunSessionFramesResponseFramesItem_Unknown)
    assert parsed.raw == raw
    high_level = parse_frame(raw)
    assert isinstance(high_level, UnknownFrame)
    assert high_level.raw == raw


@pytest.mark.parametrize("known", [_LOG, _SPAN])
def test_generated_union_rejects_complete_known_shape_without_kind(
    known: dict[str, typing.Any],
) -> None:
    kindless = {key: value for key, value in known.items() if key != "kind"}
    with pytest.raises(pydantic.ValidationError):
        parse_obj_as(RunSessionFramesResponseFramesItem, kindless)  # type: ignore[arg-type]
    with pytest.raises(pydantic.ValidationError):
        parse_frame(kindless)


def test_known_frame_constructors_preserve_default_kinds() -> None:
    log_fields: dict[str, typing.Any] = {key: value for key, value in _LOG.items() if key != "kind"}
    span_fields: dict[str, typing.Any] = {
        key: value for key, value in _SPAN.items() if key != "kind"
    }

    log = RunSessionFramesResponseFramesItem_Log(**log_fields)
    span = RunSessionFramesResponseFramesItem_Span(**span_fields)

    assert log.kind == "log"
    assert span.kind == "span"


def test_unknown_transport_variant_is_publicly_exported() -> None:
    from axilio import RunSessionFramesResponseFramesItem_Unknown as top_level_unknown
    from axilio.types import RunSessionFramesResponseFramesItem_Unknown as types_unknown

    assert top_level_unknown is RunSessionFramesResponseFramesItem_Unknown
    assert types_unknown is RunSessionFramesResponseFramesItem_Unknown


def test_generated_response_accepts_null_costs_and_mixed_frame_page() -> None:
    response: RunSessionFramesResponse = parse_obj_as(
        RunSessionFramesResponse,
        {
            "frames": [_SPAN, {"kind": "metric", "name": "cpu", "value": 0.72}, _LOG],
            "total": 3,
            "limit": 100,
            "offset": 0,
            "retention_expired": True,
            "sdk_call_costs": None,
            "inference_costs": None,
        },
    )
    assert response.sdk_call_costs is None
    assert response.inference_costs is None
    assert response.frames is not None and len(response.frames) == 3
    assert isinstance(response.frames[0], RunSessionFramesResponseFramesItem_Span)
    assert isinstance(response.frames[1], RunSessionFramesResponseFramesItem_Unknown)
    assert isinstance(response.frames[2], RunSessionFramesResponseFramesItem_Log)


def test_malformed_known_kind_cannot_fall_through_to_unknown() -> None:
    with pytest.raises(pydantic.ValidationError):
        parse_obj_as(
            RunSessionFramesResponseFramesItem,  # type: ignore[arg-type]
            {"kind": "log", "trace_id": "b" * 32},  # missing required log fields
        )


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
