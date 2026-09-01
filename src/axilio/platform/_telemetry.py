"""Live telemetry tail + trace/summary/logs helpers (AXI-1853).

The dashboard's trace viewer runs on two legs the SDK could not reach until
now: the live telemetry WebSocket (``telemetry_url`` from allocate — read-only,
one session's stream) and the durable frames archive
(``GET /phones/sessions/{id}/frames``). Both speak the unified frame envelope;
"live and archive differ only in cardinality" (live sends a span's start then
end frame; the archive returns one completed frame per span).

This module is the client half of that contract:

* ``TelemetryTail`` — iterate typed frames off the live WebSocket, with
  transparent reconnect + cursor resume (the AXI-1740 telemetry dialect:
  ``{"type": "CURSOR"}`` checkpoints, ``resume=1``/``cursor=`` attach params)
  and at-least-once replay dedupe. The session-root end frame is the
  platform's ONLY session-end signal (``peer_disconnected`` is never emitted),
  so the tail ends cleanly when it arrives — tailing doubles as event-driven
  session-end detection.
* ``SessionTelemetry`` — ``trace()`` / ``summary()`` / ``logs()`` mirroring
  the dashboard viewer, including the response-level billed-cost join
  (``sdk_call_costs`` per sdk_call span id, ``inference_costs`` per inference
  id — billed cost is a read-time billing join, never a frame attribute).

Error taxonomy is the control leg's, not a new one: a refused attach maps by
HTTP status (403 → ``SessionEndedError``: the allocation is no longer active;
401 → ``UnauthorizedError``), a drop mid-stream redials with the control
transport's full-jitter backoff, and an exhausted redial budget raises the
same retryable ``ConnectionError``.

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
import urllib.parse
from collections.abc import Callable, Iterator

import websocket

from ..drivers.mobile import _errors
from ..drivers.mobile._transport import ServerClosed, _default_ws_connect
from ..types.run_session_frames_response import RunSessionFramesResponse
from ..types.run_session_frames_response_frames_item import (
    RunSessionFramesResponseFramesItem_Log,
    RunSessionFramesResponseFramesItem_Span,
)
from ._frames import Frame, UnknownFrame, parse_frames, response_frame

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

# Telemetry-leg transport frames (AXI-1740): type-tagged (not kind-tagged) so
# they can never collide with the frame contract; consumed by the tail, never
# yielded. CURSOR is the per-batch checkpoint (opaque resume token);
# RESYNC_REQUIRED says the presented cursor predated the retained window and
# delivery continued live from the head.
_TRANSPORT_FRAME_CURSOR = "CURSOR"
_TRANSPORT_FRAME_RESYNC_REQUIRED = "RESYNC_REQUIRED"

# Redial policy, mirrored from the control transport: full-jitter exponential
# backoff, bounded consecutive attempts. Unlike a driver call (one bounded
# round-trip) a tail is long-lived, so the budget counts CONSECUTIVE failures
# and resets on every successful attach.
_MAX_REDIALS = 6
_REDIAL_BASE = 0.25
_REDIAL_CAP = 8.0

# Archive page size for trace(): the op's maximum, to minimize round-trips.
_FRAMES_PAGE_LIMIT = 1000

# Gaps shorter than this are scheduling jitter, not an unobserved interval —
# the same 5ms floor the dashboard timeline applies.
_MIN_GAP_MS = 5.0


def _redial_delay(attempt: int) -> float:
    limit = min(_REDIAL_BASE * (2**attempt), _REDIAL_CAP)
    return random.uniform(0.0, limit)


def _frame_key(frame: Frame) -> str:
    """Dedupe identity for at-least-once replay, mirroring the dashboard.

    A span reconciles on (trace_id, span_id, phase) — the contract's upsert
    key. A log has no id, so it keys on its content. An unknown frame keys on
    its raw JSON: replayed duplicates collapse, distinct unknowns survive.
    """
    if isinstance(frame, SpanFrame):
        return f"span:{frame.trace_id}:{frame.span_id}:{frame.phase}"
    if isinstance(frame, LogFrame):
        return f"log:{frame.trace_id}:{frame.span_id or ''}:{frame.time_unix_nano}:{frame.body}"
    return f"unknown:{json.dumps(frame.raw, sort_keys=True)}"


def _is_session_end(frame: Frame) -> bool:
    return (
        isinstance(frame, SpanFrame)
        and frame.phase == "end"
        and frame.span_type in _SESSION_SPAN_TYPES
    )


def _classify_refusal(e: websocket.WebSocketBadStatusException) -> _errors.AxilioError:
    """Attach HTTP status is the out-of-band liveness signal (same contract as
    the control leg): 403 means the allocation is no longer active (terminal),
    401 a bad token (terminal); anything else is a transient connect failure."""
    status = getattr(e, "status_code", None)
    if status == 403:
        return _errors.SessionEndedError(f"session is no longer active: {e}")
    if status == 401:
        return _errors.UnauthorizedError(f"telemetry token rejected: {e}")
    return _errors.ConnectionError(f"cannot connect to telemetry websocket: {e}")


class TelemetryTail:
    """Iterator over a session's live telemetry frames.

    Dial with ``iter()``/``for``; frames arrive as the generated span/log
    types or ``UnknownFrame`` (tolerant reader — an unknown kind is yielded,
    never dropped, never an error). Iteration ends cleanly when the
    session-root end frame arrives (yielded last), so::

        for frame in TelemetryTail(alloc.telemetry_url):
            ...  # the loop exiting on its own == the session is over

    Reconnects transparently on connection loss while the session lives,
    resuming from the hub's last CURSOR checkpoint; replayed frames are
    deduped, so the caller sees each frame once. Terminal conditions raise:
    ``SessionEndedError`` (attach refused with 403 — the session ended and
    the end frame is no longer obtainable live), ``UnauthorizedError`` (401),
    ``ConnectionError`` (redial budget exhausted).

    Thread-compat: one consumer per tail; ``close()`` may be called from
    another thread to stop a blocked iteration.
    """

    def __init__(
        self,
        url: str,
        *,
        open_timeout: float = 10.0,
        connect: Callable[[str, float], typing.Any] | None = None,
    ) -> None:
        if not url:
            raise ValueError("telemetry_url is empty — allocate returns it while the session lives")
        self._url = url
        self._open_timeout = open_timeout
        self._conn: typing.Any | None = None
        self._closed = False
        # Latest CURSOR checkpoint; opaque, presented verbatim on reattach.
        self._cursor = ""
        # Injectable seams (same shape as the control transport's).
        self._connect = connect or _default_ws_connect
        self._delay: Callable[[int], float] = _redial_delay

    def close(self) -> None:
        """Stop the tail. Idempotent; safe from another thread."""
        self._closed = True
        conn, self._conn = self._conn, None
        if conn is not None:
            with contextlib.suppress(Exception):
                conn.close()

    def __enter__(self) -> TelemetryTail:
        return self

    def __exit__(self, *_: object) -> None:
        self.close()

    def __iter__(self) -> Iterator[Frame]:
        seen: set[str] = set()
        redials = 0
        while not self._closed:
            try:
                conn = self._dial()
            except websocket.WebSocketBadStatusException as e:
                raise _classify_refusal(e) from e
            except (websocket.WebSocketException, OSError) as e:
                redials += 1
                if redials > _MAX_REDIALS:
                    raise _errors.ConnectionError(
                        f"cannot connect to telemetry websocket: {e}"
                    ) from e
                time.sleep(self._delay(redials - 1))
                continue
            redials = 0  # the budget covers consecutive failures only

            ended = False
            try:
                for frame in self._recv_frames(conn):
                    key = _frame_key(frame)
                    if key in seen:
                        continue  # at-least-once replay after a resume
                    seen.add(key)
                    if _is_session_end(frame):
                        ended = True
                    yield frame
                    if ended:
                        return
            except (ServerClosed, websocket.WebSocketException, OSError):
                # Connection loss (a close frame or an abrupt drop) while the
                # session may still live: redial and resume from the cursor.
                # The dedupe absorbs the at-least-once replay window. A
                # close() from another thread surfaces here too (it closes
                # the socket under the blocked recv) — then stop instead.
                self._drop_conn()

    def _dial(self) -> typing.Any:
        conn = self._connect(self._attach_url(), self._open_timeout)
        self._conn = conn
        return conn

    def _drop_conn(self) -> None:
        conn, self._conn = self._conn, None
        if conn is not None:
            with contextlib.suppress(Exception):
                conn.close()

    def _recv_frames(self, conn: typing.Any) -> Iterator[Frame]:
        """Yield contract frames off one connection until it drops.

        Transport frames (CURSOR / RESYNC_REQUIRED) are consumed here; a
        malformed message loses one live update and is dropped (the durable
        archive is unaffected), matching the dashboard viewer.
        """
        while True:
            raw = conn.recv()
            try:
                payload = json.loads(raw)
            except json.JSONDecodeError:
                continue
            if self._consume_transport(payload):
                continue
            if not isinstance(payload, dict | list):
                continue
            yield from parse_frames(payload)

    def _consume_transport(self, payload: typing.Any) -> bool:
        if not isinstance(payload, dict):
            return False
        frame_type = payload.get("type")
        if frame_type == _TRANSPORT_FRAME_CURSOR:
            cursor = payload.get("cursor")
            if isinstance(cursor, str) and cursor:
                self._cursor = cursor
            return True
        if frame_type == _TRANSPORT_FRAME_RESYNC_REQUIRED:
            # The held cursor predates the retained window: drop it rather
            # than re-present a known-stale token. The next reattach replays
            # the window from the head; the dedupe absorbs the duplicates.
            self._cursor = ""
            return True
        return False

    def _attach_url(self) -> str:
        """The telemetry URL plus the resume params (resume=1 always; the
        cursor when one is held), same construction as the control leg."""
        parts = urllib.parse.urlsplit(self._url)
        query = [
            (k, v) for k, v in urllib.parse.parse_qsl(parts.query) if k not in ("resume", "cursor")
        ]
        query.append(("resume", "1"))
        if self._cursor:
            query.append(("cursor", self._cursor))
        return urllib.parse.urlunsplit(parts._replace(query=urllib.parse.urlencode(query)))


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

    Obtained from ``Client.telemetry(session_id, telemetry_url=...)``. The
    archive views (``trace()``, ``summary()``, ``logs()``) need only the
    session id; the live ones (``tail()``, ``logs(live=True)``) need the
    ``telemetry_url`` allocate returned, which dies with the session.
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
        """Live frame iterator; see ``TelemetryTail``. The loop ending on its
        own means the session is over (the end frame is the platform's only
        session-end signal)."""
        if not self._telemetry_url:
            raise ValueError(
                "no telemetry_url for this session — pass the one allocate returned "
                "(live tailing is only possible while the allocation lives)"
            )
        return TelemetryTail(self._telemetry_url, open_timeout=open_timeout)

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
            frames.extend(response_frame(frame) for frame in page_frames)
            retention_expired = retention_expired or page.retention_expired
            # The cost maps cover the whole session on every page; merging
            # keeps this correct even if a server ever scopes them per page.
            sdk_call_costs.update(page.sdk_call_costs or {})
            inference_costs.update(page.inference_costs or {})
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
