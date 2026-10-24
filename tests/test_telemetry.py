"""Tests for the telemetry live tail + trace/summary/logs helpers.

Like test_files.py, this suite doubles as the drift pin for the hand-written
telemetry layer: everything runs through the real generated frame/response
types, so a regen that reshapes the frames surface fails here instead of in a
customer's tail.
"""

from __future__ import annotations

import json
import typing
from collections.abc import Iterator, Sequence

import httpx
import pytest

from axilio.drivers.mobile import (
    ConnectionError as SdkConnectionError,
)
from axilio.drivers.mobile import UnauthorizedError
from axilio.platform import (
    SessionNotFoundError,
    SessionTelemetry,
    TelemetryOffError,
    TelemetryTail,
    UnknownFrame,
)
from axilio.platform._frames import parse_frame
from axilio.platform._telemetry import LogFrame, SpanFrame
from axilio.types.run_session_frames_response import RunSessionFramesResponse

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


# ─── Fake stream responses ──────────────────────────────────────────────────

# A scripted open is a (status, lines) response, where a line may be an
# exception raised mid-stream (a drop), or an exception raised by the open.
Open = tuple[int, Sequence[str | Exception]] | Exception


def _event(frame: dict[str, typing.Any], *, id: str | None = None) -> list[str]:
    lines = [f"id: {id}"] if id else []
    return [*lines, f"event: {frame.get('kind', '')}", f"data: {json.dumps(frame)}", ""]


class FakeResponse:
    def __init__(self, status: int, lines: Sequence[str | Exception]) -> None:
        self.status_code = status
        self._lines = lines

    def iter_lines(self) -> Iterator[str]:
        for line in self._lines:
            if isinstance(line, Exception):
                raise line
            yield line

    def close(self) -> None:
        pass


def _tail_seq(opens: Sequence[Open]) -> tuple[TelemetryTail, list[dict[str, str]]]:
    """A tail whose Nth open follows the Nth script; records each request's
    headers."""
    requests: list[dict[str, str]] = []

    def connect(_url: str, headers: dict[str, str], _timeout: float) -> FakeResponse:
        requests.append(headers)
        script = opens[len(requests) - 1] if len(requests) <= len(opens) else OSError("no more")
        if isinstance(script, Exception):
            raise script
        return FakeResponse(*script)

    tail = TelemetryTail(
        "https://connect.test/api/v1/realtime/sessions/s1/events?token=t",
        headers={"X-Axilio-Api-Key": "axl_test"},
        connect=connect,
    )
    tail._delay = lambda _attempt: 0.0
    return tail, requests


# ─── Live tail ──────────────────────────────────────────────────────────────


def test_tail_yields_typed_frames_and_ends_on_session_end() -> None:
    tail, requests = _tail_seq(
        [
            (
                200,
                [
                    ": heartbeat",
                    "",
                    *_event(_span_wire("call-1", phase="start", end_ms=None), id="1-1"),
                    *_event(_log_wire("hello"), id="1-2"),
                    *_event({"kind": "metric", "value": 3}, id="1-3"),
                    "id: 1-4",  # a cursor-only event: no frame
                    "",
                    *_event(_SESSION_END_WIRE, id="1-5"),
                    # Anything after the end frame must never be read.
                    OSError("must not be reached"),
                ],
            )
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
    assert unknown.raw == {"kind": "metric", "value": 3}
    assert requests == [{"X-Axilio-Api-Key": "axl_test", "Accept": "text/event-stream"}]


def test_tail_reopens_with_last_event_id() -> None:
    tail, requests = _tail_seq(
        [
            (200, [*_event(_span_wire("call-a"), id="1-1"), "id: 1-2", "", OSError("drop")]),
            (200, [*_event(_span_wire("call-b"), id="1-3")]),  # the server ends the response
            (200, [*_event(_SESSION_END_WIRE, id="1-4")]),
        ]
    )
    frames = list(tail)

    assert [f.span_id for f in frames if isinstance(f, SpanFrame)] == [
        "call-a",
        "call-b",
        "sess-root",
    ]
    assert [r.get("Last-Event-ID") for r in requests] == [None, "1-2", "1-3"]


def test_tail_skips_frames_a_replay_repeats() -> None:
    # A cursor the live window has trimmed past gets the archive replayed (no
    # ids), so the reopen repeats frames the caller already has.
    tail, _ = _tail_seq(
        [
            (
                200,
                [
                    *_event(_span_wire("call-a"), id="1-1"),
                    *_event(_log_wire("hi"), id="1-2"),
                    OSError("drop"),
                ],
            ),
            (
                200,
                [
                    *_event(_span_wire("call-a")),
                    *_event(_log_wire("hi")),
                    *_event(_span_wire("call-b")),
                    *_event(_SESSION_END_WIRE, id="2-1"),
                ],
            ),
        ]
    )
    frames = list(tail)

    assert [f.span_id for f in frames if isinstance(f, SpanFrame)] == [
        "call-a",
        "call-b",
        "sess-root",
    ]
    assert [f.body for f in frames if isinstance(f, LogFrame)] == ["hi"]


@pytest.mark.parametrize(
    ("status", "error"),
    [
        (401, UnauthorizedError),
        (404, SessionNotFoundError),
        (409, TelemetryOffError),
    ],
)
def test_tail_refusal_classifies_by_http_status(status: int, error: type[Exception]) -> None:
    tail, _ = _tail_seq([(status, [])])
    with pytest.raises(error):
        list(tail)


def test_tail_ends_cleanly_on_204() -> None:
    # An ended session's stream replays and closes; the reopen gets 204.
    tail, _ = _tail_seq([(200, [*_event(_span_wire("call-a"), id="1-1")]), (204, [])])
    assert [f.span_id for f in tail if isinstance(f, SpanFrame)] == ["call-a"]


def test_tail_exhausted_reopens_raise_connection_error() -> None:
    tail, requests = _tail_seq(
        [httpx.ConnectError(f"refused {i}") for i in range(4)] + [(503, [])] * 6
    )
    with pytest.raises(SdkConnectionError):
        list(tail)
    assert len(requests) == 7  # first open + 6 reopens, the control leg's budget


def test_tail_reopen_budget_resets_after_successful_open() -> None:
    # 5 failed opens, a successful one that drops, 5 more failures, then the
    # end: consecutive counting means the tail survives 10 total failures.
    opens: list[Open] = [OSError("down") for _ in range(5)]
    opens.append((200, [*_event(_span_wire("call-a"), id="1-1"), OSError("drop")]))
    opens.extend(OSError("down") for _ in range(5))
    opens.append((200, _event(_SESSION_END_WIRE, id="1-2")))
    tail, requests = _tail_seq(opens)

    frames = list(tail)
    assert [f.span_id for f in frames if isinstance(f, SpanFrame)] == ["call-a", "sess-root"]
    assert len(requests) == 12


def test_tail_legacy_session_root_ends_stream() -> None:
    tail, _ = _tail_seq([(200, _event(_span_wire("root", span_type="phone_session", end_ms=5)))])
    assert len(list(tail)) == 1


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


class _KeyClient(_StubClient):
    base_url = "https://api.test"
    api_key = "axl_key"


def test_tail_without_telemetry_url_uses_api_host_and_key() -> None:
    tail = SessionTelemetry(_KeyClient([]), "sess-1").tail()  # type: ignore[arg-type]
    assert tail._url == "https://api.test/api/v1/realtime/sessions/sess-1/events"
    assert tail._headers == {"X-Axilio-Api-Key": "axl_key"}
