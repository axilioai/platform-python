"""Tests for the telemetry live tail + trace/summary/logs helpers.

Like test_files.py, this suite doubles as the drift pin for the hand-written
telemetry layer: everything runs through the real generated frame/response
types, so a regen that reshapes the frames surface fails here instead of in a
customer's tail.
"""

from __future__ import annotations

import json
import typing
import urllib.parse

import pytest
import websocket

from axilio.drivers.mobile import (
    ConnectionError as SdkConnectionError,
)
from axilio.drivers.mobile import (
    SessionEndedError,
    UnauthorizedError,
)
from axilio.platform import SessionTelemetry, TelemetryTail, UnknownFrame
from axilio.platform._frames import parse_frame
from axilio.platform._telemetry import LogFrame, SpanFrame
from axilio.types.run_session_frames_response import RunSessionFramesResponse
from axilio.types.run_session_frames_response_frames_item import (
    RunSessionFramesResponseFramesItem_Unknown,
)

_NS = 1_000_000  # one millisecond in nanoseconds
_BASE = 1_700_000_000_000_000_000

# ─── Wire fixtures ──────────────────────────────────────────────────────────


def _span_wire(
    span_id: str,
    *,
    phase: str = "end",
    span_type: str = "sdk_call",
    start_ms: int = 0,
    end_ms: int | None = 1,
    attributes: dict[str, typing.Any] | None = None,
) -> dict[str, typing.Any]:
    frame: dict[str, typing.Any] = {
        "kind": "span",
        "phase": phase,
        "span_type": span_type,
        "trace_id": "trace-1",
        "span_id": span_id,
        "name": span_id,
        "start_time_unix_nano": _BASE + start_ms * _NS,
    }
    if end_ms is not None:
        frame["end_time_unix_nano"] = _BASE + end_ms * _NS
        frame["status"] = {"code": "ok", "message": ""}
    if attributes:
        frame["attributes"] = attributes
    return frame


def _log_wire(body: str, *, at_ms: int = 0) -> dict[str, typing.Any]:
    return {
        "kind": "log",
        "log_type": "output_log",
        "trace_id": "trace-1",
        "time_unix_nano": _BASE + at_ms * _NS,
        "severity": "info",
        "body": body,
    }


_SESSION_END_WIRE = _span_wire("sess-root", phase="end", span_type="session", end_ms=10_000)


# ─── Fake connections ───────────────────────────────────────────────────────

# A scripted event is a JSON-encodable payload (sent as one WS message) or an
# exception instance (raised from recv, simulating a drop).
Event = dict | list | Exception


class FakeConn:
    def __init__(self, events: list[Event]) -> None:
        self._events = list(events)
        self.closed = False

    def recv(self) -> str:
        if not self._events:
            raise OSError("scripted connection exhausted")
        event = self._events.pop(0)
        if isinstance(event, Exception):
            raise event
        return json.dumps(event)

    def close(self) -> None:
        self.closed = True


def _tail_seq(dials: list[list[Event] | Exception]) -> tuple[TelemetryTail, list[str]]:
    """A tail whose Nth dial follows the Nth script: a list of recv events, or
    an exception raised from the connect attempt itself."""
    urls: list[str] = []

    def connect(url: str, _timeout: float) -> FakeConn:
        urls.append(url)
        script = dials[len(urls) - 1] if len(urls) <= len(dials) else OSError("no more dials")
        if isinstance(script, Exception):
            raise script
        return FakeConn(script)

    tail = TelemetryTail("wss://connect.test/ws/telemetry?session_id=s1&token=t", connect=connect)
    tail._delay = lambda _attempt: 0.0
    return tail, urls


def _query(url: str) -> dict[str, str]:
    return dict(urllib.parse.parse_qsl(urllib.parse.urlsplit(url).query))


# ─── Live tail ──────────────────────────────────────────────────────────────


def test_tail_yields_typed_frames_and_ends_on_session_end() -> None:
    tail, urls = _tail_seq(
        [
            [
                {"type": "CURSOR", "cursor": "c-1"},  # transport frame: consumed
                _span_wire("call-1", phase="start", end_ms=None),  # open span, single object
                [_log_wire("hello"), {"kind": "metric", "value": 3}],  # wire-array allowance
                _SESSION_END_WIRE,
                # Anything after the end frame must never be read.
                OSError("must not be reached"),
            ]
        ]
    )
    frames = list(tail)

    assert [type(f) for f in frames] == [SpanFrame, LogFrame, UnknownFrame, SpanFrame]
    open_span = frames[0]
    assert isinstance(open_span, SpanFrame)
    assert open_span.phase == "start"
    assert not open_span.end_time_unix_nano  # live start frame: still in flight
    unknown = frames[2]
    assert isinstance(unknown, UnknownFrame)
    assert unknown.kind == "metric"
    assert unknown.raw == {"kind": "metric", "value": 3}
    # One dial, resume opted in, no cursor on the first attach.
    assert len(urls) == 1
    assert _query(urls[0]) == {"session_id": "s1", "token": "t", "resume": "1"}


def test_tail_reconnects_with_cursor_and_dedupes_replay() -> None:
    span_a = _span_wire("call-a")
    tail, urls = _tail_seq(
        [
            [{"type": "CURSOR", "cursor": "c-7"}, span_a, OSError("drop")],
            # At-least-once: the window after the checkpoint replays.
            [span_a, _span_wire("call-b"), _SESSION_END_WIRE],
        ]
    )
    frames = list(tail)

    assert [f.span_id for f in frames if isinstance(f, SpanFrame)] == [
        "call-a",
        "call-b",
        "sess-root",
    ]
    assert len(urls) == 2
    assert _query(urls[1])["cursor"] == "c-7"
    assert _query(urls[1])["resume"] == "1"


def test_tail_resync_drops_stale_cursor() -> None:
    tail, urls = _tail_seq(
        [
            [{"type": "CURSOR", "cursor": "c-1"}, OSError("drop")],
            [{"type": "RESYNC_REQUIRED"}, OSError("drop")],
            [_SESSION_END_WIRE],
        ]
    )
    list(tail)
    assert "cursor" in _query(urls[1])  # held cursor presented once
    assert "cursor" not in _query(urls[2])  # dropped after RESYNC_REQUIRED


def test_tail_refused_attach_classifies_by_http_status() -> None:
    tail_403, _ = _tail_seq([websocket.WebSocketBadStatusException(f"Handshake status {403}", 403)])
    with pytest.raises(SessionEndedError):
        list(tail_403)

    tail_401, _ = _tail_seq([websocket.WebSocketBadStatusException(f"Handshake status {401}", 401)])
    with pytest.raises(UnauthorizedError):
        list(tail_401)


def test_tail_exhausted_redials_raise_connection_error() -> None:
    tail, urls = _tail_seq([OSError(f"refused {i}") for i in range(10)])
    with pytest.raises(SdkConnectionError):
        list(tail)
    assert len(urls) == 7  # first dial + 6 redials, the control leg's budget


def test_tail_redial_budget_resets_after_successful_attach() -> None:
    # 5 failed dials, a successful one that then drops, 5 more failures, then
    # the end: consecutive counting means the tail survives 10 total failures.
    dials: list[list[Event] | Exception] = [OSError("down") for _ in range(5)]
    dials.append([_span_wire("call-a"), OSError("drop")])
    dials.extend(OSError("down") for _ in range(5))
    dials.append([_SESSION_END_WIRE])
    tail, urls = _tail_seq(dials)

    frames = list(tail)
    assert [f.span_id for f in frames if isinstance(f, SpanFrame)] == ["call-a", "sess-root"]
    assert len(urls) == 12


def test_tail_legacy_session_root_ends_stream() -> None:
    tail, _ = _tail_seq([[_span_wire("root", span_type="phone_session", end_ms=5)]])
    frames = list(tail)
    assert len(frames) == 1


def test_parse_frame_live_start_allowance() -> None:
    # A start-phase frame describes an open span: no end_time_unix_nano, no
    # status on the wire. It must parse as a typed span, not error.
    frame = parse_frame(_span_wire("call-1", phase="start", end_ms=None))
    assert isinstance(frame, SpanFrame)
    assert frame.end_time_unix_nano == 0
    assert frame.status is not None and frame.status.code == ""


# ─── Archive views ──────────────────────────────────────────────────────────


class _StubRuns:
    def __init__(self, pages: list[RunSessionFramesResponse]) -> None:
        self._pages = pages
        self.calls: list[dict[str, int]] = []

    def sessions_list_frames(
        self, session_id: str, *, limit: int, offset: int
    ) -> RunSessionFramesResponse:
        assert session_id == "sess-1"
        self.calls.append({"limit": limit, "offset": offset})
        index = min(len(self.calls) - 1, len(self._pages) - 1)
        return self._pages[index]


class _StubClient:
    def __init__(self, pages: list[RunSessionFramesResponse]) -> None:
        self.runs = _StubRuns(pages)

    @property
    def raw(self) -> _StubClient:
        return self


def _page(
    frames: list[typing.Any],
    *,
    total: int,
    offset: int,
    sdk_call_costs: dict[str, int] | None = None,
    inference_costs: dict[str, int] | None = None,
) -> RunSessionFramesResponse:
    return RunSessionFramesResponse(
        frames=frames,
        total=total,
        limit=1000,
        offset=offset,
        retention_expired=False,
        sdk_call_costs=sdk_call_costs or {},
        inference_costs=inference_costs or {},
    )


def _span(
    span_id: str,
    *,
    span_type: str = "sdk_call",
    start_ms: int = 0,
    end_ms: int = 1,
    attributes: dict[str, typing.Any] | None = None,
):
    return parse_frame(
        _span_wire(
            span_id, span_type=span_type, start_ms=start_ms, end_ms=end_ms, attributes=attributes
        )
    )


def _log(body: str, *, at_ms: int):
    return parse_frame(_log_wire(body, at_ms=at_ms))


def test_trace_joins_costs_and_paginates() -> None:
    session_span = _span("root", span_type="session", start_ms=0, end_ms=10_000)
    call = _span("call-1", start_ms=1000, end_ms=2000)
    inference = _span(
        "inf-span",
        span_type="inference",
        start_ms=1100,
        end_ms=1900,
        attributes={"axilio.inference.id": "inf-9"},
    )
    log = _log("line", at_ms=500)
    costs = {"sdk_call_costs": {"call-1": 700}, "inference_costs": {"inf-9": 450}}
    pages = [
        _page([session_span, call], total=4, offset=0, **costs),
        _page([inference, log], total=4, offset=2, **costs),
    ]
    client = _StubClient(pages)

    trace = SessionTelemetry(client, "sess-1").trace()  # type: ignore[arg-type]

    assert client.runs.calls == [{"limit": 1000, "offset": 0}, {"limit": 1000, "offset": 2}]
    by_id = {ts.frame.span_id: ts for ts in trace.spans}
    assert by_id["call-1"].billed_cost_microdollars == 700
    assert by_id["inf-span"].billed_cost_microdollars == 450
    assert by_id["root"].billed_cost_microdollars is None
    # Ordered by start time regardless of page arrival order.
    assert [ts.frame.span_id for ts in trace.spans] == ["root", "call-1", "inf-span"]
    assert [log_frame.body for log_frame in trace.logs] == ["line"]


def test_trace_coalesces_null_cost_maps() -> None:
    page = RunSessionFramesResponse(
        frames=[],
        total=0,
        limit=1000,
        offset=0,
        retention_expired=True,
        sdk_call_costs=None,
        inference_costs=None,
    )
    trace = SessionTelemetry(_StubClient([page]), "sess-1").trace()  # type: ignore[arg-type]
    assert trace.retention_expired
    assert trace.sdk_call_costs == {}
    assert trace.inference_costs == {}


def test_trace_maps_generated_unknown_variant_to_public_unknown_frame() -> None:
    generated = RunSessionFramesResponseFramesItem_Unknown(
        kind="metric", name="cpu.utilization", value=0.72
    )  # type: ignore[call-arg]
    page = _page([_span("call-1"), generated, _log("done", at_ms=2)], total=3, offset=0)
    trace = SessionTelemetry(_StubClient([page]), "sess-1").trace()  # type: ignore[arg-type]
    assert len(trace.spans) == 1
    assert len(trace.logs) == 1
    assert len(trace.unknown) == 1
    assert trace.unknown[0].kind == "metric"
    assert trace.unknown[0].raw == {
        "kind": "metric",
        "name": "cpu.utilization",
        "value": 0.72,
    }


def test_summary_math_mirrors_dashboard() -> None:
    session_span = _span("root", span_type="session", start_ms=0, end_ms=10_000)
    call_1 = _span("call-1", start_ms=1000, end_ms=2000)
    call_2 = _span("call-2", start_ms=2500, end_ms=3000)
    pages = [
        _page(
            [session_span, call_1, call_2, _log("tail", at_ms=9000)],
            total=4,
            offset=0,
            sdk_call_costs={"call-1": 700},
        )
    ]
    summary = SessionTelemetry(_StubClient(pages), "sess-1").summary()  # type: ignore[arg-type]

    assert summary.total_ms == pytest.approx(10_000)
    assert summary.sdk_ms == pytest.approx(1500)
    # Gaps: 0→1000, 2000→2500, 3000→10000 (the idle tail counts).
    assert summary.unobserved_ms == pytest.approx(8500)
    assert summary.call_count == 2
    assert summary.billable_call_count == 1
    assert summary.billed_cost_microdollars == 700


def test_summary_duration_prefers_producer_clock() -> None:
    # The source-measured axilio.duration_ns wins over wall-clock end−start.
    call = _span("call-1", start_ms=1000, end_ms=2000, attributes={"axilio.duration_ns": 250 * _NS})
    pages = [_page([call], total=1, offset=0)]
    trace = SessionTelemetry(_StubClient(pages), "sess-1").trace()  # type: ignore[arg-type]
    assert trace.spans[0].duration_ms == pytest.approx(250)


def test_logs_archive_filters_and_orders() -> None:
    pages = [
        _page(
            [_log("b", at_ms=200), _span("call-1"), _log("a", at_ms=100)],
            total=3,
            offset=0,
        )
    ]
    logs = list(SessionTelemetry(_StubClient(pages), "sess-1").logs())  # type: ignore[arg-type]
    assert [log_frame.body for log_frame in logs] == ["a", "b"]


def test_tail_requires_telemetry_url() -> None:
    with pytest.raises(ValueError):
        SessionTelemetry(_StubClient([]), "sess-1").tail()  # type: ignore[arg-type]
