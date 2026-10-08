"""Tests for RemoteTransport — the DCP control-WebSocket transport."""

from __future__ import annotations

import _thread
import base64
import hashlib
import json
import re
import socket
import threading
import time
from collections.abc import Callable
from typing import Any

import pytest
import websocket

from axilio.drivers.mobile import (
    ActionTimeoutError,
    ControlHeldError,
    DeviceOfflineError,
    MobileDriver,
    RemoteTransport,
    SessionEndedError,
    StrategyUnavailableError,
    UnauthorizedError,
)
from axilio.drivers.mobile import (
    ConnectionError as SdkConnectionError,
)
from axilio.drivers.mobile import (
    TimeoutError as SdkTimeoutError,
)
from axilio.drivers.mobile._transport import ServerClosed

Responder = Callable[[dict[str, Any]], list[dict[str, Any]]]


class FakeWS:
    """A scripted in-memory WebSocket: each sent frame runs `responder`,
    whose returned frames are queued for subsequent `recv()` calls."""

    def __init__(self, responder: Responder) -> None:
        self.responder = responder
        self.url = ""
        self.sent: list[dict[str, Any]] = []
        self.timeout: float | None = None
        self.closed = False
        self._inbox: list[dict[str, Any]] = []
        self.preloaded: list[dict[str, Any]] = []

    def settimeout(self, t: float | None) -> None:
        self.timeout = t

    def send(self, text: str) -> None:
        frame = json.loads(text)
        self.sent.append(frame)
        self._inbox.extend(self.responder(frame))

    def recv(self) -> str:
        if self.preloaded:
            return json.dumps(self.preloaded.pop(0))
        if not self._inbox:
            raise websocket.WebSocketConnectionClosedException("no more frames")
        return json.dumps(self._inbox.pop(0))

    def close(self) -> None:
        self.closed = True

    def abort(self) -> None:
        self.closed = True


def _reply_result(result: Any) -> Responder:
    return lambda frame: [{"id": frame["id"], "result": result}]


def _transport_with(responder: Responder) -> tuple[RemoteTransport, list[FakeWS]]:
    """Build a RemoteTransport whose connect factory yields fresh FakeWS
    instances (so reconnects are observable)."""
    conns: list[FakeWS] = []

    def connect(url: str, _timeout: float) -> FakeWS:
        ws = FakeWS(responder)
        ws.url = url
        conns.append(ws)
        return ws

    rt = RemoteTransport("wss://connect.test/ws/control?token=x", connect=connect)
    rt._delay = lambda _attempt: 0.0  # keep the redial matrix instant
    return rt, conns


def _transport_seq(responders: list[Responder]) -> tuple[RemoteTransport, list[FakeWS]]:
    """Like _transport_with, but each (re)dial gets its own responder, the
    scripted-connection seam the force-close matrix drives."""
    conns: list[FakeWS] = []

    def connect(url: str, _timeout: float) -> FakeWS:
        assert len(conns) < len(responders), "unexpected extra dial"
        ws = FakeWS(responders[len(conns)])
        ws.url = url
        conns.append(ws)
        return ws

    rt = RemoteTransport("wss://connect.test/ws/control?token=x", connect=connect)
    rt._delay = lambda _attempt: 0.0
    return rt, conns


def _key_of(frame: dict[str, Any]) -> str | None:
    return (frame.get("params") or {}).get("idempotencyKey")


def test_call_sends_cdp_frame_and_returns_result() -> None:
    rt, conns = _transport_with(_reply_result({"ok": True}))
    out = rt.call("Touch.tap", {"x": 540, "y": 1180})
    assert out == {"ok": True}
    frame = conns[0].sent[0]
    assert frame["id"] == 1
    assert frame["method"] == "Touch.tap"
    # Mutating input carries a transport-minted idempotency key; the
    # caller's own params ride unchanged beside it.
    assert frame["params"]["x"] == 540
    assert frame["params"]["y"] == 1180
    assert _key_of(frame)


def test_call_omits_params_when_none() -> None:
    rt, conns = _transport_with(_reply_result({"png_base64": "Zg=="}))
    rt.call("Screen.screenshot")
    assert conns[0].sent[0] == {"id": 1, "method": "Screen.screenshot"}


def test_ids_increment_per_call() -> None:
    rt, conns = _transport_with(_reply_result({}))
    rt.call("Touch.tap", {"x": 1, "y": 2})
    rt.call("Touch.tap", {"x": 3, "y": 4})
    assert [f["id"] for f in conns[0].sent] == [1, 2]


@pytest.mark.parametrize("method", ["Locator.tap", "Locator.fill", "Locator.press"])
def test_locator_mutating_methods_carry_idempotency_key(method: str) -> None:
    """Locator.tap/fill/press act on the device, so they need the same
    dedup-on-resend guarantee as Touch/Keyboard, even though they share a
    domain with the read-only Locator.* methods below."""
    rt, conns = _transport_with(_reply_result({"tookMs": 5}))
    rt.call(method, {"locator": {"text": "Continue"}})
    assert _key_of(conns[0].sent[0])


@pytest.mark.parametrize(
    "method", ["Locator.waitFor", "Locator.boundingBox", "Locator.text", "Locator.count"]
)
def test_locator_read_methods_carry_no_idempotency_key(method: str) -> None:
    """The rest of the Locator domain only reads/waits; keeping them keyless
    matches every other read (Screen.observe, Locator.boundingBox, ...)."""
    rt, conns = _transport_with(_reply_result({"tookMs": 5}))
    rt.call(method, {"locator": {"text": "Continue"}})
    assert _key_of(conns[0].sent[0]) is None


def test_notifications_are_skipped_before_reply() -> None:
    def responder(frame: dict[str, Any]) -> list[dict[str, Any]]:
        return [
            {"method": "Log.entry", "params": {"level": "info"}},  # no id → skipped
            {"id": frame["id"], "result": {"ok": True}},
        ]

    rt, _ = _transport_with(responder)
    assert rt.call("Touch.tap", {"x": 1, "y": 2}) == {"ok": True}


def test_error_frame_maps_to_exception() -> None:
    def responder(frame: dict[str, Any]) -> list[dict[str, Any]]:
        return [
            {
                "id": frame["id"],
                "error": {
                    "code": -32004,
                    "message": "device offline",
                    "data": {"kind": "DeviceOffline", "retryable": True},
                },
            }
        ]

    rt, _ = _transport_with(responder)
    with pytest.raises(DeviceOfflineError) as ei:
        rt.call("Touch.tap", {"x": 1, "y": 2})
    assert ei.value.retryable is True


def test_action_timeout_kind_maps_and_is_a_builtin_timeout_error() -> None:
    def responder(frame: dict[str, Any]) -> list[dict[str, Any]]:
        return [
            {
                "id": frame["id"],
                "error": {
                    "code": -32009,
                    "message": "target never became actionable",
                    "data": {"kind": "ActionTimeout", "retryable": False},
                },
            }
        ]

    rt, _ = _transport_with(responder)
    with pytest.raises(ActionTimeoutError) as ei:
        rt.call("Locator.tap", {"locator": {"text": "Continue"}})
    assert ei.value.retryable is False
    # Also catchable as the builtin TimeoutError, since that's what it is.
    assert isinstance(ei.value, TimeoutError)


def test_strategy_unavailable_kind_maps() -> None:
    def responder(frame: dict[str, Any]) -> list[dict[str, Any]]:
        return [
            {
                "id": frame["id"],
                "error": {
                    "code": -32010,
                    "message": "no accessibility tree on this session",
                    "data": {"kind": "StrategyUnavailable"},
                },
            }
        ]

    rt, _ = _transport_with(responder)
    with pytest.raises(StrategyUnavailableError):
        rt.call("Locator.tap", {"locator": {"role": "button"}})


def test_timeout_drops_conn_and_next_call_reconnects() -> None:
    calls = 0

    def responder(frame: dict[str, Any]) -> list[dict[str, Any]]:
        nonlocal calls
        calls += 1
        if calls == 1:
            raise websocket.WebSocketTimeoutException("slow")
        return [{"id": frame["id"], "result": {"ok": True}}]

    rt, conns = _transport_with(responder)
    with pytest.raises(SdkTimeoutError):
        rt.call("Screen.observe", {"ocr_engine": "free"}, timeout=0.1)
    assert conns[0].closed is True
    # The SAME transport recovers: its next call opens a fresh connection
    # (a timeout drops the socket so a late reply can't be misread).
    assert rt.call("Screen.observe", {"ocr_engine": "free"}) == {"ok": True}
    assert len(conns) == 2


def test_closed_connection_surfaces_connection_error() -> None:
    rt, conns = _transport_with(lambda _frame: [])  # never replies → recv finds empty inbox
    with pytest.raises(SdkConnectionError):
        rt.call("Touch.tap", {"x": 1, "y": 2})
    assert conns[0].closed is True


def test_close_is_idempotent() -> None:
    rt, conns = _transport_with(_reply_result({}))
    rt.call("Touch.tap", {"x": 1, "y": 2})
    rt.close()
    rt.close()
    assert conns[0].closed is True


def test_driver_over_remote_emits_cdp_methods() -> None:
    """The driver's helpers should put DCP method names on the wire."""
    rt, conns = _transport_with(_reply_result({}))
    drv = MobileDriver(rt)
    drv.tap({"x": 5, "y": 6})
    drv.type_text("hi")
    by_method = {f["method"]: f.get("params") or {} for f in conns[0].sent}
    assert by_method["Touch.tap"]["x"] == 5
    assert by_method["Touch.tap"]["y"] == 6
    assert by_method["Keyboard.typeText"]["text"] == "hi"


# --- the reconnect contract (AXI-1727) --------------------------------------


def _closing_responder(exc: Exception) -> Responder:
    def responder(_frame: dict[str, Any]) -> list[dict[str, Any]]:
        raise exc

    return responder


@pytest.mark.parametrize(
    "close_exc",
    [
        ServerClosed(1001, "Server shutting down"),
        ServerClosed(1013, "Server shutting down"),
        ServerClosed(1011, "welcome send failed"),
        websocket.WebSocketConnectionClosedException("abrupt loss"),
    ],
    ids=["1001-going-away", "1013-try-again-later", "1011-internal-error", "abrupt-loss"],
)
def test_retryable_close_redials_and_resends_exactly_once(close_exc: Exception) -> None:
    """The force-close matrix, retryable half: the interrupted command is
    re-sent on a fresh connection under a fresh id with the SAME
    idempotency key, so the caller's tap succeeds exactly once (the
    executor's ledger dedups on the key)."""
    rt, conns = _transport_seq([_closing_responder(close_exc), _reply_result({"ok": True})])
    assert rt.call("Touch.tap", {"x": 120, "y": 640}) == {"ok": True}
    assert len(conns) == 2
    original, resend = conns[0].sent[0], conns[1].sent[0]
    assert resend["method"] == "Touch.tap"
    key = _key_of(original)
    assert key and key == _key_of(resend), "one key, minted once, reused verbatim on the re-send"
    assert resend["id"] > original["id"], "ids stay monotonic across the redial"


@pytest.mark.parametrize(
    ("close_exc", "expected"),
    [
        (ServerClosed(1000, "session ended"), SessionEndedError),
        (ServerClosed(1000, "Superseded"), SessionEndedError),
        (ServerClosed(4409, "control_held:editor"), ControlHeldError),
    ],
    ids=["1000-session-ended", "1000-superseded", "4409-control-held"],
)
def test_terminal_close_surfaces_without_redial(
    close_exc: Exception, expected: type[Exception]
) -> None:
    """Terminal half of the matrix: 1000 and 4409 surface their class with
    zero redials; retrying a dead session (or a held lease) is forbidden
    by contract."""
    rt, conns = _transport_seq([_closing_responder(close_exc), _reply_result({})])
    with pytest.raises(expected) as ei:
        rt.call("Touch.tap", {"x": 1, "y": 2})
    assert ei.value.retryable is False  # type: ignore[attr-defined]
    assert len(conns) == 1, "a terminal close must never be auto-retried"


@pytest.mark.parametrize(
    ("status", "expected"),
    [(403, SessionEndedError), (401, UnauthorizedError)],
    ids=["403-session-over", "401-bad-token"],
)
def test_reattach_http_status_is_terminal(status: int, expected: type[Exception]) -> None:
    """Reattach HTTP status is the out-of-band liveness signal: 403 means
    the allocation is gone, 401 a bad token; both end the redial loop."""
    conns: list[FakeWS] = []

    def connect(url: str, _timeout: float) -> FakeWS:
        if conns:
            raise websocket.WebSocketBadStatusException("handshake refused", status)
        ws = FakeWS(_closing_responder(ServerClosed(1001, "going away")))
        ws.url = url
        conns.append(ws)
        return ws

    rt = RemoteTransport("wss://connect.test/ws/control?token=x", connect=connect)
    rt._delay = lambda _attempt: 0.0
    with pytest.raises(expected):
        rt.call("Touch.tap", {"x": 1, "y": 2})


def test_cursor_tracked_and_presented_on_reattach() -> None:
    """Every attach opts in with resume=1; a reattach presents the latest
    Axilio.cursor checkpoint so delivery resumes where this client left
    off."""
    calls = 0

    def responder(frame: dict[str, Any]) -> list[dict[str, Any]]:
        nonlocal calls
        calls += 1
        if calls == 1:
            return [
                {"method": "Axilio.cursor", "params": {"cursor": "1755861234567-0"}},
                {"id": frame["id"], "result": {}},
            ]
        raise ServerClosed(1001, "going away")

    rt, conns = _transport_seq([responder, _reply_result({})])
    rt.call("Touch.tap", {"x": 1, "y": 2})
    rt.call("Touch.tap", {"x": 3, "y": 4})
    assert len(conns) == 2
    assert "resume=1" in conns[0].url and "cursor=" not in conns[0].url
    assert "resume=1" in conns[1].url and "cursor=1755861234567-0" in conns[1].url


def test_resync_clears_cursor() -> None:
    """Axilio.resyncRequired means the held cursor predates the retained
    window; it must be dropped, not re-presented on the next reattach."""
    calls = 0

    def responder(frame: dict[str, Any]) -> list[dict[str, Any]]:
        nonlocal calls
        calls += 1
        if calls == 1:
            return [
                {"method": "Axilio.cursor", "params": {"cursor": "5-0"}},
                {
                    "method": "Axilio.resyncRequired",
                    "params": {"requested": "5-0", "oldest": "9-0"},
                },
                {"id": frame["id"], "result": {}},
            ]
        raise ServerClosed(1001, "going away")

    rt, conns = _transport_seq([responder, _reply_result({})])
    rt.call("Touch.tap", {"x": 1, "y": 2})
    rt.call("Touch.tap", {"x": 3, "y": 4})
    assert "cursor=" not in conns[1].url


def test_stale_replayed_response_skipped() -> None:
    """AXI-1293 regression, resumed-connection flavor: a pre-drop response
    redelivered on the resumed socket must never be matched to the re-sent
    command: the transport matches strictly by the fresh id."""
    rt, conns = _transport_seq(
        [
            _closing_responder(ServerClosed(1001, "going away")),
            lambda frame: [{"id": frame["id"], "result": {"source": "fresh"}}],
        ]
    )

    def connect_preload(_url: str, _timeout: float) -> None:  # pragma: no cover
        raise AssertionError("unused")

    # The stale replay: the pre-drop response for the ORIGINAL id arrives
    # first on the resumed connection (at-least-once redelivery).
    out_of_band = {"id": 1, "result": {"source": "stale-replay"}}
    original_connect = rt._connect

    def connect(url: str, timeout: float) -> FakeWS:
        ws = original_connect(url, timeout)
        assert isinstance(ws, FakeWS)
        if len(conns) == 2:
            ws.preloaded.append(out_of_band)
        return ws

    rt._connect = connect
    assert rt.call("Screen.observe") == {"source": "fresh"}
    assert conns[1].sent[0]["id"] > conns[0].sent[0]["id"]


def test_handshake_replayed_on_reattach() -> None:
    """A handshake performed by the caller is replayed internally after a
    reattach, before the interrupted command resumes: capability state is
    per-connection."""
    result = {
        "protocol_version": 1,
        "device": {
            "device_id": "d1",
            "platform": "android",
            "form_factor": "phone",
            "input_modalities": ["touch"],
            "screen_width": 1080,
            "screen_height": 2400,
        },
        "domains": ["Touch"],
        "capabilities": ["Touch.tap"],
    }

    def respond_all(frame: dict[str, Any]) -> list[dict[str, Any]]:
        if frame["method"] == "Protocol.handshake":
            return [{"id": frame["id"], "result": result}]
        return [{"id": frame["id"], "result": {}}]

    calls = 0

    def conn1_responder(frame: dict[str, Any]) -> list[dict[str, Any]]:
        nonlocal calls
        calls += 1
        if calls == 1:
            return respond_all(frame)
        raise ServerClosed(1001, "going away")

    rt, conns = _transport_seq([conn1_responder, respond_all])
    rt.call("Protocol.handshake", {})
    rt.call("Touch.tap", {"x": 1, "y": 2})
    assert [f["method"] for f in conns[1].sent] == ["Protocol.handshake", "Touch.tap"]


def test_redial_budget_is_bounded() -> None:
    """Persistent dial failure surfaces a retryable ConnectionError after
    initial + 6 redials, never an unbounded loop."""
    dials = 0

    def connect(_url: str, _timeout: float) -> FakeWS:
        nonlocal dials
        dials += 1
        raise OSError("connect unreachable")

    rt = RemoteTransport("wss://connect.test/ws/control?token=x", connect=connect)
    rt._delay = lambda _attempt: 0.0
    with pytest.raises(SdkConnectionError) as ei:
        rt.call("Touch.tap", {"x": 1, "y": 2})
    assert ei.value.retryable is True
    assert dials == 7  # initial + _MAX_REDIALS


def test_keys_only_on_mutating_methods() -> None:
    """Reads stay keyless by contract: they are naturally safe to re-send,
    and keyless reads keep the executor's dedup ledger small."""
    rt, conns = _transport_with(_reply_result({}))
    rt.call("Touch.tap", {"x": 1, "y": 2})
    rt.call("Screen.observe")
    assert _key_of(conns[0].sent[0])
    assert _key_of(conns[0].sent[1]) is None


# --- interruptible waits (AXI-2226) -------------------------------------------


class _SlowWS(FakeWS):
    """A FakeWS whose first `slow` reads time out, as a socket timeout surfaces.

    It records every read timeout it was given.
    """

    def __init__(self, responder: Responder, slow: int) -> None:
        super().__init__(responder)
        self.slow = slow
        self.read_timeouts: list[float | None] = []

    def recv(self) -> str:
        self.read_timeouts.append(self.timeout)
        if self.slow > 0:
            self.slow -= 1
            raise websocket.WebSocketTimeoutException("timed out")
        return super().recv()


def test_untimed_call_waits_in_short_slices_until_the_reply() -> None:
    ws = _SlowWS(_reply_result({"ok": True}), slow=5)
    rt = RemoteTransport("wss://connect.test/ws/control?token=x", connect=lambda _u, _t: ws)
    assert rt.call("Screen.observe", {"ocr_engine": "free"}) == {"ok": True}
    # No deadline: five empty slices are waited through, never one long block.
    assert len(ws.read_timeouts) == 6
    assert all(t is not None and t <= 0.5 for t in ws.read_timeouts)


def test_timed_call_still_honors_its_deadline() -> None:
    ws = _SlowWS(_reply_result({"ok": True}), slow=10**9)
    rt = RemoteTransport("wss://connect.test/ws/control?token=x", connect=lambda _u, _t: ws)
    started = time.monotonic()
    with pytest.raises(SdkTimeoutError) as excinfo:
        rt.call("Screen.observe", {"ocr_engine": "free"}, timeout=0.2)
    assert str(excinfo.value) == "Screen.observe timed out after 0.2s"
    assert time.monotonic() - started < 2
    assert ws.closed is True


def test_interrupted_call_drops_the_connection_and_the_next_call_reconnects() -> None:
    conns: list[FakeWS] = []

    class _InterruptedWS(FakeWS):
        def recv(self) -> str:
            raise KeyboardInterrupt

    def connect(_url: str, _timeout: float) -> FakeWS:
        first = not conns
        ws: FakeWS = (
            _InterruptedWS(_reply_result({})) if first else FakeWS(_reply_result({"ok": 1}))
        )
        conns.append(ws)
        return ws

    rt = RemoteTransport("wss://connect.test/ws/control?token=x", connect=connect)
    with pytest.raises(KeyboardInterrupt):
        rt.call("Screen.observe", {"ocr_engine": "free"})
    # The abandoned reply may be half read: the socket is dropped, not reused.
    assert conns[0].closed is True
    assert rt.call("Screen.observe", {"ocr_engine": "free"}) == {"ok": 1}
    assert len(conns) == 2


def test_connection_without_abort_is_refused_on_connect() -> None:
    """A timed-out call drops its connection with abort, so a factory whose
    connections lack it fails on the first call instead of leaking them."""

    class _NoAbortWS:
        def settimeout(self, t: float | None) -> None:
            pass

        def send(self, text: str) -> None:
            pass

        def recv(self) -> str:
            return ""

        def close(self) -> None:
            pass

    rt = RemoteTransport(
        "wss://connect.test/ws/control?token=x", connect=lambda _u, _t: _NoAbortWS()
    )
    with pytest.raises(TypeError) as excinfo:
        rt.call("Screen.observe", {"ocr_engine": "free"})
    assert str(excinfo.value) == (
        "connect returned a _NoAbortWS, which lacks one of "
        "send / recv / settimeout / close / abort"
    )


class _ScriptedWSServer:
    """Accepts one WebSocket, completes the handshake, then runs `script`.

    Use it as a context manager: leaving the block closes the listening
    socket, so a failed test can't leave the serving thread waiting.
    """

    _GUID = b"258EAFA5-E914-47DA-95CA-C5AB0DC85B11"

    def __init__(self, script: Callable[[socket.socket], None]) -> None:
        self._script = script
        self._listener = socket.create_server(("127.0.0.1", 0))
        self.url = f"ws://127.0.0.1:{self._listener.getsockname()[1]}/ws/control?token=x"
        self._thread = threading.Thread(target=self._serve, daemon=True)

    def __enter__(self) -> _ScriptedWSServer:
        self._thread.start()
        return self

    def __exit__(self, *_exc: object) -> None:
        self._listener.close()

    def _serve(self) -> None:
        try:
            conn, _ = self._listener.accept()
        except OSError:
            return  # the test ended before connecting, and __exit__ closed the listener
        with conn:
            request = b""
            while b"\r\n\r\n" not in request:
                request += conn.recv(4096)
            match = re.search(rb"Sec-WebSocket-Key: *(\S+)", request, re.IGNORECASE)
            assert match is not None
            accept = base64.b64encode(hashlib.sha1(match.group(1) + self._GUID).digest())
            conn.sendall(
                b"HTTP/1.1 101 Switching Protocols\r\nUpgrade: websocket\r\n"
                b"Connection: Upgrade\r\nSec-WebSocket-Accept: " + accept + b"\r\n\r\n"
            )
            try:
                self._script(conn)
            except (BrokenPipeError, ConnectionResetError):
                return  # the client gave up and dropped the socket, as these tests expect


def _stay_silent(_conn: socket.socket) -> None:
    # Never answer. Give up after five seconds, so a regression fails the
    # test instead of hanging the run.
    time.sleep(5)


def _trickle_reply(conn: socket.socket) -> None:
    # The reply to the first call (id 1) as one unmasked text frame, sent a
    # byte at a time: every socket read succeeds well inside any timeout.
    payload = json.dumps({"id": 1, "result": {"ok": True}}).encode()
    for byte in bytes([0x81, len(payload)]) + payload:
        conn.sendall(bytes([byte]))
        time.sleep(0.1)


def test_ctrl_c_interrupts_a_call_waiting_on_a_silent_server() -> None:
    # A real websocket-client connection that never gets a reply.
    # interrupt_main() raises the pending KeyboardInterrupt the way Ctrl+C
    # does on Windows: it can't wake a blocking socket read, only the
    # interpreter between operations. One long blocking read would hold it
    # until the server gives up five seconds later.
    with _ScriptedWSServer(_stay_silent) as server:
        rt = RemoteTransport(server.url, open_timeout=5)
        timer = threading.Timer(0.5, _thread.interrupt_main)
        started = time.monotonic()
        timer.start()
        try:
            with pytest.raises(KeyboardInterrupt):
                rt.call("Screen.observe", {"ocr_engine": "free"})
        finally:
            timer.cancel()
        assert time.monotonic() - started < 3


def test_trickled_reply_cannot_outlast_the_call_deadline() -> None:
    # The reply takes about 3 s to arrive in full, but no single socket read
    # waits long. A per-read timeout alone would keep assembling the frame
    # past the 0.6 s deadline and return it late.
    with _ScriptedWSServer(_trickle_reply) as server:
        rt = RemoteTransport(server.url, open_timeout=5)
        started = time.monotonic()
        with pytest.raises(SdkTimeoutError) as excinfo:
            rt.call("Screen.observe", {"ocr_engine": "free"}, timeout=0.6)
        assert time.monotonic() - started < 2
    assert str(excinfo.value) == "Screen.observe timed out after 0.6s"
