"""Live telemetry tail + trace/summary/logs helpers (AXI-1853, AXI-2975).

The dashboard's trace viewer runs on two legs: the session's event stream
(``telemetry_url``: Server-Sent Events on the realtime host, read-only, one
session's frames) and the durable frames archive
(``GET /phones/sessions/{id}/frames``). Both speak the unified frame envelope;
"live and archive differ only in cardinality" (live sends a span's start then
end frame; the archive returns one completed frame per span).

This module is the client half of that contract:

* ``TelemetryTail`` iterates typed frames off the event stream. The server does
  the bookkeeping: a fresh stream starts with the archived trace, then the live
  frames, deduplicated on span id and phase. A dropped stream reopens with
  ``Last-Event-ID`` and resumes with no gap. The tail ends cleanly on the
  session-root end frame, or when the server answers 204 (the session is over
  and nothing is left), so tailing doubles as event-driven session-end
  detection.
* ``SessionTelemetry`` — ``trace()`` / ``summary()`` / ``logs()`` mirroring
  the dashboard viewer, including the response-level billed-cost join
  (``sdk_call_costs`` per sdk_call span id, ``inference_costs`` per inference
  id — billed cost is a read-time billing join, never a frame attribute).

Errors: a refused stream maps by HTTP status (401/403 → ``UnauthorizedError``,
404 → ``SessionNotFoundError``, 409 → ``TelemetryOffError``); a drop reopens
with the control transport's full-jitter backoff, and an exhausted budget
raises the retryable ``ConnectionError``.

Hand-written and preserved across ``fern generate`` via ``src/axilio/.fernignore``.
Like ``_files.py``, ``tests/test_telemetry.py`` doubles as the drift pin: it
drives these helpers through the real generated response types, so a regen
that reshapes the frames surface breaks CI instead of a customer.
"""

from __future__ import annotations

import contextlib
import dataclasses
import json
import random
import time
import typing
from collections.abc import Callable, Iterable, Iterator

import httpx

from ..drivers.mobile import _errors
from ..types.run_session_frames_response import RunSessionFramesResponse
from ..types.run_session_frames_response_frames_item import (
    RunSessionFramesResponseFramesItem_Log,
    RunSessionFramesResponseFramesItem_Span,
)
from ._frames import Frame, UnknownFrame, parse_frame

if typing.TYPE_CHECKING:  # pragma: no cover — import cycle guard, types only
    from . import Client

SpanFrame = RunSessionFramesResponseFramesItem_Span
LogFrame = RunSessionFramesResponseFramesItem_Log

# The session-root span types (unified frame contract): "session" is the
# device-neutral root, "phone_session" the pre-2026-08-21 stored value a
# tolerant reader still recognizes.
_SESSION_SPAN_TYPES = frozenset({"session", "phone_session"})

_SPAN_TYPE_SDK_CALL = "sdk_call"
_SPAN_TYPE_INFERENCE = "inference"
_ATTR_INFERENCE_ID = "axilio.inference.id"
_ATTR_DURATION_NS = "axilio.duration_ns"

# Reopen policy, mirrored from the control transport: full-jitter exponential
# backoff, bounded consecutive attempts. A tail is long-lived, so the budget
# counts CONSECUTIVE failures and resets on every successful open.
_MAX_REDIALS = 6
_REDIAL_BASE = 0.25
_REDIAL_CAP = 8.0

# The server sends a heartbeat every 15 s, so this much silence means a dead
# connection; the read times out and the tail reopens from its cursor.
_IDLE_TIMEOUT = 45.0

_API_KEY_HEADER = "X-Axilio-Api-Key"

# Archive page size for trace(): the op's maximum, to minimize round-trips.
_FRAMES_PAGE_LIMIT = 1000

# Gaps shorter than this are scheduling jitter, not an unobserved interval —
# the same 5ms floor the dashboard timeline applies.
_MIN_GAP_MS = 5.0


class SessionNotFoundError(_errors.AxilioError):
    """No such session in the caller's organization (HTTP 404)."""

    code = "not_found"


class TelemetryOffError(_errors.AxilioError):
    """The session was started with telemetry off, so nothing is streamed or
    stored (HTTP 409)."""

    code = "telemetry_off"


def _redial_delay(attempt: int) -> float:
    limit = min(_REDIAL_BASE * (2**attempt), _REDIAL_CAP)
    return random.uniform(0.0, limit)


def _is_session_end(frame: Frame) -> bool:
    return (
        isinstance(frame, SpanFrame)
        and frame.phase == "end"
        and frame.span_type in _SESSION_SPAN_TYPES
    )


def _refusal(status: int) -> _errors.AxilioError | None:
    """The terminal error for a refused stream, or None when the status is
    transient (5xx and the like) and worth another open."""
    if status in (401, 403):
        return _errors.UnauthorizedError(f"telemetry credential rejected (HTTP {status})")
    if status == 404:
        return SessionNotFoundError("session not found (HTTP 404)")
    if status == 409:
        return TelemetryOffError("telemetry is off for this session (HTTP 409)")
    return None


class _Response(typing.Protocol):
    status_code: int

    def iter_lines(self) -> Iterator[str]: ...

    def close(self) -> None: ...


class _HttpxResponse:
    """One streaming GET; closing it also closes its client."""

    def __init__(self, client: httpx.Client, response: httpx.Response) -> None:
        self._client = client
        self._response = response
        self.status_code = response.status_code

    def iter_lines(self) -> Iterator[str]:
        return self._response.iter_lines()

    def close(self) -> None:
        with contextlib.suppress(Exception):
            self._response.close()
        self._client.close()


def _default_open(url: str, headers: dict[str, str], open_timeout: float) -> _Response:
    client = httpx.Client(timeout=httpx.Timeout(open_timeout, read=_IDLE_TIMEOUT))
    try:
        response = client.send(client.build_request("GET", url, headers=headers), stream=True)
    except BaseException:
        client.close()
        raise
    return _HttpxResponse(client, response)


@dataclasses.dataclass
class _Event:
    id: str | None = None
    data: list[str] = dataclasses.field(default_factory=list)


def _events(lines: Iterable[str]) -> Iterator[_Event]:
    """Server-sent events per the SSE spec: field lines up to a blank line,
    comments (``:``) ignored, multi-line data joined by the caller."""
    event = _Event()
    seen = False
    for line in lines:
        if line == "":
            if seen:
                yield event
            event, seen = _Event(), False
            continue
        if line.startswith(":"):
            continue
        name, _, value = line.partition(":")
        value = value.removeprefix(" ")
        seen = True
        if name == "id":
            event.id = value
        elif name == "data":
            event.data.append(value)


class TelemetryTail:
    """Iterator over a session's telemetry frames.

    Iterate with ``for``; frames arrive as the generated span/log types or
    ``UnknownFrame`` (tolerant reader — an unknown kind is yielded, never
    dropped, never an error). Iteration ends cleanly when the session is over,
    so::

        for frame in TelemetryTail(alloc.telemetry_url):
            ...  # the loop exiting on its own == the session is over

    A dropped stream reopens with ``Last-Event-ID`` and resumes exactly; the
    server deduplicates, so each frame arrives once. Terminal conditions
    raise: ``UnauthorizedError``, ``SessionNotFoundError``,
    ``TelemetryOffError``, and ``ConnectionError`` once the reopen budget is
    spent.

    ``headers`` go on every request, for example ``X-Axilio-Api-Key`` when
    the URL carries no token. Thread-compat: one consumer per tail;
    ``close()`` may be called from another thread to stop a blocked
    iteration.
    """

    def __init__(
        self,
        url: str,
        *,
        headers: dict[str, str] | None = None,
        open_timeout: float = 10.0,
        connect: Callable[[str, dict[str, str], float], _Response] | None = None,
    ) -> None:
        if not url:
            raise ValueError("telemetry_url is empty")
        self._url = url
        self._headers = dict(headers or {})
        self._open_timeout = open_timeout
        self._response: _Response | None = None
        self._closed = False
        self._cursor = ""
        # Injectable seams (same shape as the control transport's).
        self._connect = connect or _default_open
        self._delay: Callable[[int], float] = _redial_delay

    def close(self) -> None:
        """Stop the tail. Idempotent; safe from another thread."""
        self._closed = True
        self._drop()

    def __enter__(self) -> TelemetryTail:
        return self

    def __exit__(self, *_: object) -> None:
        self.close()

    def __iter__(self) -> Iterator[Frame]:
        failures = 0
        while not self._closed:
            try:
                response = self._connect(self._url, self._request_headers(), self._open_timeout)
            except (httpx.HTTPError, OSError) as e:
                failures = self._backoff(failures, e)
                continue
            if response.status_code != 200:
                response.close()
                if response.status_code == 204:
                    return  # the session is over and nothing is left
                refusal = _refusal(response.status_code)
                if refusal is not None:
                    raise refusal
                failures = self._backoff(failures, f"HTTP {response.status_code}")
                continue
            failures = 0  # the budget covers consecutive failures only
            self._response = response
            try:
                for event in _events(response.iter_lines()):
                    if event.id is not None:
                        self._cursor = event.id
                    frame = _frame_of(event)
                    if frame is None:
                        continue
                    yield frame
                    if _is_session_end(frame):
                        return
            except (httpx.HTTPError, OSError):
                # A drop (or a close() from another thread, which the loop
                # condition then catches): reopen from the cursor.
                pass
            finally:
                self._drop()

    def _backoff(self, failures: int, cause: object) -> int:
        failures += 1
        if failures > _MAX_REDIALS:
            raise _errors.ConnectionError(f"cannot open telemetry stream: {cause}")
        time.sleep(self._delay(failures - 1))
        return failures

    def _drop(self) -> None:
        response, self._response = self._response, None
        if response is not None:
            with contextlib.suppress(Exception):
                response.close()

    def _request_headers(self) -> dict[str, str]:
        headers = {**self._headers, "Accept": "text/event-stream"}
        if self._cursor:
            headers["Last-Event-ID"] = self._cursor
        return headers


def _frame_of(event: _Event) -> Frame | None:
    """The frame an event carries, or None for a cursor-only event or data
    that is not a frame object (dropped, like the dashboard viewer)."""
    if not event.data:
        return None
    try:
        payload = json.loads("\n".join(event.data))
    except json.JSONDecodeError:
        return None
    if not isinstance(payload, dict):
        return None
    return parse_frame(payload)


# ─── Archive-side views (trace / summary / logs) ────────────────────────────


@dataclasses.dataclass(frozen=True)
class TraceSpan:
    """One completed (or in-flight) span with its billed cost joined in.

    ``billed_cost_microdollars`` is the post-markup figure the invoice
    charges: for an sdk_call span it comes from ``sdk_call_costs[span_id]``,
    for an inference span from ``inference_costs[axilio.inference.id]``
    (the per-inference detail behind its parent call's cost); None means
    "nothing billed for this span".
    """

    frame: SpanFrame
    billed_cost_microdollars: int | None

    @property
    def duration_ms(self) -> float:
        """Span duration, preferring the source-measured ``axilio.duration_ns``
        (a monotonic clock at the producer) over wall-clock end−start."""
        return _span_duration_ms(self.frame)


@dataclasses.dataclass(frozen=True)
class Trace:
    """The dashboard trace view's data, reconstructed client-side."""

    spans: list[TraceSpan]
    logs: list[LogFrame]
    unknown: list[UnknownFrame]
    retention_expired: bool
    sdk_call_costs: dict[str, int]
    inference_costs: dict[str, int]


@dataclasses.dataclass(frozen=True)
class TraceSummary:
    """The trace header rollup: where the session's time and money went.

    ``unobserved_ms`` is every interval not covered by an sdk_call — a sleep,
    an OCR loop, an untraced network call. It is never labeled beyond that:
    there is no instrumentation for what the caller's code was doing.
    """

    total_ms: float
    sdk_ms: float
    unobserved_ms: float
    call_count: int
    billable_call_count: int
    billed_cost_microdollars: int


class SessionTelemetry:
    """A session's telemetry surface: live tail + archive-backed views.

    Obtained from ``Client.telemetry(session_id, telemetry_url=...)``. Every
    view needs only the session id. The live ones (``tail()``,
    ``logs(live=True)``) use ``telemetry_url`` when given, and otherwise the
    session's stream on the API host with the client's API key.
    """

    def __init__(
        self,
        client: Client,
        session_id: str,
        telemetry_url: str | None = None,
    ) -> None:
        self._client = client
        self._session_id = session_id
        self._telemetry_url = telemetry_url

    @property
    def session_id(self) -> str:
        return self._session_id

    def tail(self, *, open_timeout: float = 10.0) -> TelemetryTail:
        """Frame iterator over the session's event stream; see
        ``TelemetryTail``. It replays the trace so far, then follows live, and
        the loop ending on its own means the session is over. Works for an
        ended session too (it replays the trace and ends)."""
        from . import _API_PREFIX  # the Client's module; imported here to avoid a cycle

        url = self._telemetry_url or (
            f"{self._client.base_url}{_API_PREFIX}/realtime/sessions/{self._session_id}/events"
        )
        return TelemetryTail(
            url,
            headers={_API_KEY_HEADER: self._client.api_key},
            open_timeout=open_timeout,
        )

    def trace(self) -> Trace:
        """The full durable trace: collapsed spans ordered by start time with
        billed costs joined, logs ordered by time, unknown frames preserved."""
        frames: list[Frame] = []
        retention_expired = False
        sdk_call_costs: dict[str, int] = {}
        inference_costs: dict[str, int] = {}
        offset = 0
        while True:
            page = self._list_frames(limit=_FRAMES_PAGE_LIMIT, offset=offset)
            page_frames = page.frames or []
            frames.extend(page_frames)
            retention_expired = retention_expired or page.retention_expired
            # The cost maps cover the whole session on every page; merging
            # keeps this correct even if a server ever scopes them per page.
            sdk_call_costs.update(page.sdk_call_costs)
            inference_costs.update(page.inference_costs)
            offset += len(page_frames)
            if not page_frames or offset >= page.total:
                break

        spans = _collapse_spans(frames)
        spans.sort(key=lambda s: s.start_time_unix_nano)
        logs = sorted(
            (f for f in frames if isinstance(f, LogFrame)), key=lambda f: f.time_unix_nano
        )
        unknown = [f for f in frames if isinstance(f, UnknownFrame)]
        return Trace(
            spans=[
                TraceSpan(
                    frame=s,
                    billed_cost_microdollars=_billed_cost(s, sdk_call_costs, inference_costs),
                )
                for s in spans
            ],
            logs=logs,
            unknown=unknown,
            retention_expired=retention_expired,
            sdk_call_costs=sdk_call_costs,
            inference_costs=inference_costs,
        )

    def summary(self) -> TraceSummary:
        """The trace header rollup, computed exactly as the dashboard does."""
        return summarize(self.trace())

    def logs(self, *, live: bool = False) -> Iterator[LogFrame]:
        """The session's log frames (output lines, errors, kernel status).

        ``live=False`` reads the durable archive; ``live=True`` tails the
        live stream, ending when the session does.
        """
        if not live:
            return iter(self.trace().logs)
        return (f for f in self.tail() if isinstance(f, LogFrame))

    def _list_frames(self, *, limit: int, offset: int) -> RunSessionFramesResponse:
        return self._client.raw.runs.sessions_list_frames(
            self._session_id, limit=limit, offset=offset
        )


def summarize(trace: Trace) -> TraceSummary:
    """Compute the header rollup from a trace, mirroring the dashboard.

    Anchored on the session-root span when present (the true lease
    lifecycle), else the earliest frame; the timeline ends at the latest span
    end / log time, so the idle tail counts. An in-flight sdk_call (no end
    yet) stretches to the timeline end. Unobserved intervals under 5ms are
    scheduling jitter and don't count.
    """
    span_frames = [ts.frame for ts in trace.spans]
    session_span = next((s for s in span_frames if s.span_type in _SESSION_SPAN_TYPES), None)
    start_nanos = [s.start_time_unix_nano for s in span_frames if s.start_time_unix_nano > 0]
    start_nanos += [log.time_unix_nano for log in trace.logs if log.time_unix_nano > 0]
    if session_span is not None:
        anchor = session_span.start_time_unix_nano
    else:
        anchor = min(start_nanos) if start_nanos else 0

    def offset_ms(nano: int | None) -> float:
        if not anchor or not nano:
            return 0.0
        return max(0.0, (nano - anchor) / 1e6)

    end_ms = 0.0
    for s in span_frames:
        end_ms = max(end_ms, offset_ms(s.end_time_unix_nano or s.start_time_unix_nano))
    for log in trace.logs:
        end_ms = max(end_ms, offset_ms(log.time_unix_nano))

    # One (start, duration) interval per sdk_call; a running call stretches to
    # the timeline end.
    calls: list[tuple[float, float]] = []
    for ts in trace.spans:
        s = ts.frame
        if s.span_type != _SPAN_TYPE_SDK_CALL:
            continue
        start = offset_ms(s.start_time_unix_nano)
        duration = ts.duration_ms if s.end_time_unix_nano else max(0.0, end_ms - start)
        calls.append((start, duration))
    calls.sort(key=lambda c: c[0])

    sdk_ms = sum(d for _, d in calls)
    unobserved_ms = 0.0
    cursor = 0.0
    for start, duration in calls:
        if start - cursor >= _MIN_GAP_MS:
            unobserved_ms += start - cursor
        cursor = max(cursor, start + duration)
    if end_ms - cursor >= _MIN_GAP_MS:
        unobserved_ms += end_ms - cursor

    billable = [
        ts.billed_cost_microdollars
        for ts in trace.spans
        if ts.frame.span_type == _SPAN_TYPE_SDK_CALL and (ts.billed_cost_microdollars or 0) > 0
    ]
    return TraceSummary(
        total_ms=max(1.0, end_ms),
        sdk_ms=sdk_ms,
        unobserved_ms=unobserved_ms,
        call_count=len(calls),
        billable_call_count=len(billable),
        billed_cost_microdollars=sum(c for c in billable if c),
    )


def _collapse_spans(frames: list[Frame]) -> list[SpanFrame]:
    """One span per span_id: the end frame wins over the start (live sends
    both; the archive sends end only, so this is a no-op there)."""
    by_id: dict[str, SpanFrame] = {}
    for f in frames:
        if not isinstance(f, SpanFrame):
            continue
        prev = by_id.get(f.span_id)
        if prev is None or (prev.phase != "end" and f.phase == "end"):
            by_id[f.span_id] = f
    return list(by_id.values())


def _billed_cost(
    span: SpanFrame,
    sdk_call_costs: dict[str, int],
    inference_costs: dict[str, int],
) -> int | None:
    if span.span_type == _SPAN_TYPE_SDK_CALL:
        return sdk_call_costs.get(span.span_id)
    if span.span_type == _SPAN_TYPE_INFERENCE:
        inference_id = (span.attributes or {}).get(_ATTR_INFERENCE_ID)
        if isinstance(inference_id, str) and inference_id:
            return inference_costs.get(inference_id)
    return None


def _span_duration_ms(span: SpanFrame) -> float:
    raw_ns = (span.attributes or {}).get(_ATTR_DURATION_NS)
    if isinstance(raw_ns, int | float) and raw_ns > 0:
        return float(raw_ns) / 1e6
    if isinstance(raw_ns, str):
        try:
            parsed = float(raw_ns)
        except ValueError:
            parsed = 0.0
        if parsed > 0:
            return parsed / 1e6
    end = span.end_time_unix_nano
    if end and end > span.start_time_unix_nano:
        return (end - span.start_time_unix_nano) / 1e6
    return 0.0
