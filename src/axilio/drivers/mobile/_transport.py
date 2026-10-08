"""Transport seam + the in-sandbox SandboxTransport."""

from __future__ import annotations

import contextlib
import json
import os
import random
import socket
import threading
import time
import urllib.parse
import uuid
from collections.abc import Callable
from typing import Any, Protocol, cast, runtime_checkable

import websocket  # websocket-client: synchronous WS client for RemoteTransport

from . import _envelope, _errors

_DEFAULT_SOCKET_PATH = "/run/axilio/sdk.sock"
_ENV_SOCKET_PATH = "AXILIO_SDK_SOCKET"


@runtime_checkable
class Transport(Protocol):
    """The seam every driver call goes through. One round-trip per call.

    ``method`` is a DCP method name ("Domain.method", e.g. "Touch.tap",
    "Screen.observe") — the driver's helpers translate their ergonomic API
    to these, the same way Playwright's helpers translate to CDP. Both
    transports send the method verbatim; only the framing differs
    (WebSocket messages vs newline-delimited JSON on the daemon socket).
    """

    def call(
        self,
        method: str,
        args: dict[str, Any] | None = None,
        *,
        timeout: float | None = None,
    ) -> dict[str, Any] | None: ...

    def close(self) -> None: ...


# --- DCP frame codec, shared by both transports -----------------------
# A command rides the wire as {"id", "method", "params"}; the reply echoes
# the id with exactly one of "result" / "error". SandboxTransport frames
# these as one JSON object per line; RemoteTransport as one per WebSocket
# message.


def _build_frame(req_id: int, method: str, args: dict[str, Any] | None) -> dict[str, Any]:
    frame: dict[str, Any] = {"id": req_id, "method": method}
    if args is not None:
        frame["params"] = args
    return frame


def _decode_frame(text: str) -> dict[str, Any]:
    try:
        return json.loads(text)
    except json.JSONDecodeError as e:
        raise _errors.InternalError(f"malformed JSON frame: {e}") from e


def _unwrap_reply(msg: dict[str, Any]) -> dict[str, Any] | None:
    error = msg.get("error")
    if error is not None:
        raise _errors.from_dcp_error(error)
    return msg.get("result")


class SandboxTransport:
    """`Transport` over the in-VM daemon's Unix socket — DCP frames, one
    JSON object per line."""

    def __init__(self, socket_path: str | None = None) -> None:
        self._socket_path: str = (
            socket_path or os.environ.get(_ENV_SOCKET_PATH) or _DEFAULT_SOCKET_PATH
        )
        self._lock = threading.Lock()
        self._sock: socket.socket | None = None
        self._buf = b""
        self._next_id = 0

    @property
    def socket_path(self) -> str:
        return self._socket_path

    def call(
        self,
        method: str,
        args: dict[str, Any] | None = None,
        *,
        timeout: float | None = None,
    ) -> dict[str, Any] | None:
        """Send a DCP command, wait for the id-matched reply, return its result."""
        with self._lock:
            self._ensure_connected()
            assert self._sock is not None
            self._next_id += 1
            req_id = self._next_id
            try:
                if timeout is not None:
                    self._sock.settimeout(timeout)
                self._send(_build_frame(req_id, method, args))
                msg = self._recv()
                # Skip stale replies from abandoned calls (id < ours). The
                # daemon answers every command it reads; if an earlier call
                # was interrupted after sending but before its reply was
                # consumed, that reply is still queued on the socket and
                # arrives first. Higher/odd ids are genuine protocol bugs.
                while isinstance(msg.get("id"), int) and msg["id"] < req_id:
                    msg = self._recv()
            except TimeoutError as e:
                self._close_locked()
                raise _errors.TimeoutError(f"{method} timed out after {timeout}s") from e
            except OSError as e:
                self._close_locked()
                raise _errors.ConnectionError(f"socket I/O failed: {e}") from e
            except BaseException:
                # Anything else — KeyboardInterrupt from a notebook cell
                # cancel while a call blocks, cancellation, a decode error —
                # abandons this call with its reply possibly still in
                # flight. Drop the connection so the late reply can't be
                # misread as the next call's; reconnect is lazy.
                self._close_locked()
                raise
            finally:
                if self._sock is not None and timeout is not None:
                    with contextlib.suppress(OSError):
                        self._sock.settimeout(None)
        # The daemon is strictly request/response (no notifications) and
        # stale lower ids were skipped above, so any remaining mismatch is
        # a protocol bug.
        if msg.get("id") != req_id:
            raise _errors.InternalError(f"id mismatch: sent {req_id!r}, got {msg.get('id')!r}")
        return _unwrap_reply(msg)

    def close(self) -> None:
        """Close the underlying socket. Idempotent."""
        with self._lock:
            self._close_locked()

    def _ensure_connected(self) -> None:
        if self._sock is not None:
            return
        # CPython on Windows has no AF_UNIX. The daemon socket only exists
        # inside an Axilio sandbox (a Linux VM), so say where to go instead of
        # surfacing a bare AttributeError.
        family = getattr(socket, "AF_UNIX", None)
        if family is None:
            raise _errors.ConnectionError(
                "SandboxTransport needs a Unix socket and only runs inside an Axilio sandbox; "
                "outside one, use client.session() or MobileDriver.connect_remote()"
            )
        try:
            sock = socket.socket(family, socket.SOCK_STREAM)
            sock.connect(self._socket_path)
        except (FileNotFoundError, ConnectionRefusedError, PermissionError) as e:
            raise _errors.ConnectionError(
                f"cannot connect to {self._socket_path}: {e}. "
                "Is the daemon running and is this code executing inside an Axilio sandbox?"
            ) from e
        self._sock = sock
        self._buf = b""

    def _close_locked(self) -> None:
        if self._sock is not None:
            with contextlib.suppress(OSError):
                self._sock.close()
            self._sock = None
            self._buf = b""

    def _send(self, frame: dict[str, Any]) -> None:
        assert self._sock is not None
        line = (json.dumps(frame) + "\n").encode("utf-8")
        self._sock.sendall(line)

    def _recv(self) -> dict[str, Any]:
        assert self._sock is not None
        while b"\n" not in self._buf:
            chunk = self._sock.recv(4096)
            if not chunk:
                raise OSError("daemon closed the connection")
            self._buf += chunk
        line, _, rest = self._buf.partition(b"\n")
        self._buf = rest
        return _decode_frame(line.decode("utf-8"))


@runtime_checkable
class _WSConn(Protocol):
    """What RemoteTransport needs from a connection its factory returns.

    abort closes at once, without the close handshake. A connection from an
    injected factory is checked against this when it arrives.
    """

    def send(self, text: str) -> None: ...

    def recv(self) -> str: ...

    def settimeout(self, t: float | None) -> None: ...

    def close(self) -> None: ...

    def abort(self) -> None: ...


class ServerClosed(Exception):
    """The server closed the WebSocket with a close frame.

    Raised by a connection's ``recv`` so the transport can classify the
    close code (retryable vs terminal). ``code`` is None for an abrupt
    loss with no close frame.
    """

    def __init__(self, code: int | None, reason: str = "") -> None:
        super().__init__(f"control websocket closed: {code} {reason}".strip())
        self.code = code
        self.reason = reason


# Reconnect contract constants (the transport notifications ride the vendor
# Axilio domain, below the CDP frame, and are opt-in via resume=1).
_METHOD_AXILIO_CURSOR = "Axilio.cursor"
_METHOD_AXILIO_RESYNC_REQUIRED = "Axilio.resyncRequired"

# 4409: another controller holds the session's control lease. Terminal:
# a retry loop against a held lease is the one-controller model's failure
# mode.
_CLOSE_CONTROL_HELD = 4409

# Close codes the redial loop recovers: 1001 going away (shutdown / ping
# timeout), 1013 try again later (draining pod), 1011 internal error.
# Abrupt loss (no close frame) classifies retryable too.
_RETRYABLE_CLOSE_CODES = frozenset({1001, 1011, 1013})

# Bounded redial: full-jitter exponential backoff sized for an interactive
# SDK call: the worst accumulated wait (~15s across the budget) stays
# inside a default call deadline while covering a connect pod replacement.
_MAX_REDIALS = 6
_REDIAL_BASE = 0.25
_REDIAL_CAP = 8.0

# Longest single wait for a reply frame. A call waits in slices of at most
# this long until its deadline (or indefinitely without one), so a pending
# KeyboardInterrupt surfaces within about this long: on Windows a blocking
# socket read does not return for Ctrl+C, the interpreter only raises it
# between operations.
_RECV_SLICE_S = 0.5

# The interaction domains are the mutating input surface; only their
# commands carry idempotency keys (reads are naturally safe, and keyless
# reads keep the executor's dedup ledger small). Touch and Keyboard are
# mutating domain-wide; Locator mixes mutating actions (tap/fill/press)
# with reads (waitFor/boundingBox/text/count) in the same domain, so those
# three are named individually instead.
_MUTATING_DOMAINS = frozenset({"Touch", "Keyboard"})
_MUTATING_METHODS = frozenset({"Locator.tap", "Locator.fill", "Locator.press"})


def _redial_delay(attempt: int) -> float:
    limit = min(_REDIAL_BASE * (2**attempt), _REDIAL_CAP)
    return random.uniform(0.0, limit)


def _is_mutating_method(method: str) -> bool:
    if method in _MUTATING_METHODS:
        return True
    domain, _, rest = method.partition(".")
    return bool(rest) and domain in _MUTATING_DOMAINS


class RemoteTransport:
    """`Transport` over the DCP control WebSocket — literal CDP frames.

    The driver already speaks DCP method names, so this transport does no
    name translation: each call goes out as a CDP request
    ``{"id", "method", "params"}`` and the matching ``{"id", "result"|"error"}``
    comes back — the same wire an off-the-shelf CDP client speaks. One
    WebSocket per allocation; the allocation lease outlives the socket, so
    a drop is recovered rather than surfaced (the reconnect contract):

    - Every attach opts in to cursor checkpoints (``resume=1``); the
      transport tracks the latest ``Axilio.cursor`` and presents it on
      reattach, so the server resumes delivery where this client left off.
    - A retryable close (1001/1013/1011, abrupt loss) triggers a bounded
      backoff redial against the same URL (the control token deliberately
      outlives the session cap). A terminal close (1000 session ended /
      superseded, 4409 control held) or a 403/401 on reattach surfaces
      immediately and is never auto-retried.
    - The one in-flight command is re-sent after a successful reattach
      under a fresh request id; mutating input carries a transport-minted
      ``idempotencyKey`` (reused verbatim on the re-send), so the executor
      dedups and the command executes exactly once.
    - Request ids stay monotonic across redials: a resumed socket can
      still deliver a pre-drop response, and a reused id would mismatch it
      to the wrong call.
    - A handshake performed by the caller is replayed internally after
      every reattach before work resumes: capability state is
      per-connection.
    """

    def __init__(
        self,
        url: str,
        *,
        open_timeout: float = 10.0,
        connect: Any | None = None,
    ) -> None:
        self._url = url
        self._open_timeout = open_timeout
        self._lock = threading.Lock()
        self._conn: _WSConn | None = None
        self._next_id = 0
        # Latest Axilio.cursor checkpoint, the opaque resume token
        # presented on reattach. Empty until the first checkpoint (or after
        # a resync, whose window the server could not replay).
        self._cursor = ""
        # Params of the last successful Protocol.handshake, for the
        # internal replay after a reattach. None until the caller performs
        # one.
        self._handshake_args: dict[str, Any] | None = None
        # Injectable seams: the connection factory (url, open_timeout) ->
        # conn (a _WSConn), and the backoff schedule (tests shrink it to keep the
        # force-close matrix fast).
        self._connect: Callable[[str, float], object] = connect or _default_ws_connect
        self._delay: Callable[[int], float] = _redial_delay

    def call(
        self,
        method: str,
        args: dict[str, Any] | None = None,
        *,
        timeout: float | None = None,
    ) -> dict[str, Any] | None:
        """Send a CDP command, await the id-matched reply, return its result."""
        with self._lock:
            # The idempotency key is minted once per logical command and
            # reused verbatim on every re-send of it, which is what lets
            # the executor's ledger answer a duplicate without executing
            # twice.
            if _is_mutating_method(method):
                args = dict(args or {})
                args.setdefault("idempotencyKey", str(uuid.uuid4()))

            redials = 0
            while True:
                try:
                    result = self._attempt(method, args, timeout)
                except _errors.ConnectionError as e:
                    if not e.retryable:
                        raise
                    redials += 1
                    if redials > _MAX_REDIALS:
                        raise
                    time.sleep(self._delay(redials - 1))
                    continue
                if method == _envelope.METHOD_PROTOCOL_HANDSHAKE:
                    self._handshake_args = dict(args or {})
                return result

    def close(self) -> None:
        """Close the underlying WebSocket. Idempotent."""
        with self._lock:
            self._close_locked()

    def _attempt(
        self,
        method: str,
        args: dict[str, Any] | None,
        timeout: float | None,
    ) -> dict[str, Any] | None:
        """One connect-if-needed + send + await round of the call.

        A retryable connection failure raises ConnectionError with
        ``retryable=True`` for the caller's redial loop; everything else is
        final for the call.
        """
        conn = self._ensure_connected()
        self._next_id += 1
        req_id = self._next_id
        frame = _build_frame(req_id, method, args)
        # No timeout means no deadline, on every call. Before, an untimed
        # call inherited the open timeout until the first timed call and
        # waited forever after it.
        deadline = None if timeout is None else time.monotonic() + timeout
        # A send only blocks once the network has stalled; without a call
        # deadline it is bounded like the connect step.
        send_limit = timeout if timeout is not None else self._open_timeout
        try:
            conn.settimeout(send_limit)
            conn.send(json.dumps(frame))
            return self._await_reply(conn, req_id, deadline)
        except websocket.WebSocketTimeoutException as e:
            # Dropped so a late reply can't be misread. No close handshake:
            # waiting on a server that just timed out would add up to 3s.
            self._close_locked(abort=True)
            raise _errors.TimeoutError(f"{method} timed out after {send_limit}s") from e
        except ServerClosed as e:
            self._close_locked()
            raise _classify_close(e) from e
        except _errors.AxilioError:
            # A DCP error frame the executor sent back (`_unwrap_reply` inside
            # `_await_reply` already mapped it); not a transport failure.
            # `ActionTimeoutError` in particular is also a builtin
            # `TimeoutError`, itself an `OSError` subclass, so it would
            # otherwise fall into the broad catch below and get misreported
            # as a connection loss.
            raise
        except (websocket.WebSocketException, OSError) as e:
            # Abrupt loss with no close frame: same as 1001 by contract.
            self._close_locked()
            raise _errors.ConnectionError(f"control websocket I/O failed: {e}") from e
        except BaseException:
            # Deliberately broad, and always re-raised: anything else that
            # leaves here (Ctrl+C's KeyboardInterrupt above all) abandons the
            # call with its reply in flight, possibly mid-frame. Drop the
            # connection so a half-read frame is never parsed as the next
            # reply; the next call reconnects and resumes.
            self._close_locked(abort=True)
            raise

    def _recv(self, conn: _WSConn, deadline: float | None) -> str:
        """One frame, waited for in slices of at most _RECV_SLICE_S.

        A single blocking read can't be interrupted by Ctrl+C on Windows, so
        the wait is a loop of short reads. Between them the interpreter can
        raise a pending KeyboardInterrupt. websocket-client keeps a partly
        read frame across a read that times out, so a slice ending mid-frame
        resumes cleanly on the next one.
        """
        while True:
            wait = _RECV_SLICE_S
            if deadline is not None:
                remaining = deadline - time.monotonic()
                if remaining <= 0:
                    raise websocket.WebSocketTimeoutException("call deadline passed")
                wait = min(wait, remaining)
            conn.settimeout(wait)
            try:
                raw: str = conn.recv()
            except websocket.WebSocketTimeoutException:
                continue
            return raw

    def _await_reply(
        self, conn: _WSConn, req_id: int, deadline: float | None
    ) -> dict[str, Any] | None:
        # Read until the frame that echoes our id. Id-less frames are
        # notifications: the Axilio.* transport notifications are
        # intercepted (cursor tracking, resync) before the skip, everything
        # else is skipped. Stale responses (a pre-drop reply redelivered
        # after a resume) have older ids and are skipped by the same
        # match, never mismatched to this call.
        while True:
            raw = self._recv(conn, deadline)
            if not raw:
                raise websocket.WebSocketConnectionClosedException("control websocket closed")
            text = raw if isinstance(raw, str) else raw.decode("utf-8")
            msg = _decode_frame(text)
            if msg.get("id") is None:
                self._observe_notification(msg)
                continue
            if msg.get("id") != req_id:
                continue
            return _unwrap_reply(msg)

    def _observe_notification(self, msg: dict[str, Any]) -> None:
        method = msg.get("method")
        params = msg.get("params") or {}
        if method == _METHOD_AXILIO_CURSOR:
            cursor = params.get("cursor")
            if isinstance(cursor, str) and cursor:
                self._cursor = cursor
        elif method == _METHOD_AXILIO_RESYNC_REQUIRED:
            # The retained window expired: the server could not replay the
            # gap and continued live. Nothing is lost on this
            # request/response path, because the transport never relies on
            # replayed responses (the in-flight command is always re-sent
            # and the executor dedups); but the held cursor predates the
            # window, so drop it rather than re-present a known-stale token.
            self._cursor = ""

    def _ensure_connected(self) -> _WSConn:
        if self._conn is None:
            try:
                conn = self._connect(self._attach_url(), self._open_timeout)
            except websocket.WebSocketBadStatusException as e:
                raise _classify_bad_status(e) from e
            except (websocket.WebSocketException, OSError) as e:
                raise _errors.ConnectionError(f"cannot connect to control websocket: {e}") from e
            if not isinstance(conn, _WSConn):
                raise TypeError(
                    f"connect returned a {type(conn).__name__}, which lacks one of "
                    "send / recv / settimeout / close / abort"
                )
            self._conn = conn
            # Capability state is per-connection: replay the caller's
            # handshake before any command resumes on the new socket.
            if self._handshake_args is not None:
                self._replay_handshake(self._conn)
        return self._conn

    def _replay_handshake(self, conn: _WSConn) -> None:
        self._next_id += 1
        req_id = self._next_id
        frame = _build_frame(req_id, _envelope.METHOD_PROTOCOL_HANDSHAKE, self._handshake_args)
        try:
            # Part of reconnecting, so bounded like the connect step.
            conn.settimeout(self._open_timeout)
            conn.send(json.dumps(frame))
            self._await_reply(conn, req_id, time.monotonic() + self._open_timeout)
        except ServerClosed as e:
            self._close_locked()
            raise _classify_close(e) from e
        except _errors.AxilioError:
            # See the matching guard in `_attempt`: a mapped DCP error, not
            # a transport failure.
            raise
        except (websocket.WebSocketException, OSError) as e:
            self._close_locked()
            raise _errors.ConnectionError(f"handshake replay failed: {e}") from e
        except BaseException:
            # Deliberately broad, and always re-raised: same as an abandoned
            # call in _attempt.
            self._close_locked(abort=True)
            raise

    def _attach_url(self) -> str:
        """The control URL plus the resume params.

        Every attach opts in to checkpoints (resume=1); a reattach that
        holds a cursor presents it so delivery continues where this client
        left off. The same URL stays valid across redials by design; the
        control token outlives the session cap.
        """
        parts = urllib.parse.urlsplit(self._url)
        query = urllib.parse.parse_qsl(parts.query)
        query = [(k, v) for k, v in query if k not in ("resume", "cursor")]
        query.append(("resume", "1"))
        if self._cursor:
            query.append(("cursor", self._cursor))
        return urllib.parse.urlunsplit(parts._replace(query=urllib.parse.urlencode(query)))

    def _close_locked(self, *, abort: bool = False) -> None:
        """Drop the connection.

        abort skips the close handshake, whose wait for the server's reply
        (up to 3s) would only delay a caller who timed out or was interrupted.
        """
        conn, self._conn = self._conn, None
        if conn is None:
            return
        # Detached first, so a close that raises can't leave the next call on
        # this connection. A socket error from the close is moot, the
        # connection is gone either way; anything else is a bug in the
        # connection and surfaces, chained to the error being handled.
        with contextlib.suppress(OSError, websocket.WebSocketException):
            if abort:
                conn.abort()
            else:
                conn.close()


def _classify_close(e: ServerClosed) -> _errors.AxilioError:
    """Map a server close frame onto the contract's close-code classes."""
    if e.code == 1000:
        # "session ended", or this connection was superseded by a newer
        # one. Either way this transport is done.
        return _errors.SessionEndedError(str(e))
    if e.code == _CLOSE_CONTROL_HELD:
        return _errors.ControlHeldError(str(e))
    # 1001 / 1013 / 1011 / anything else: retryable connection loss.
    return _errors.ConnectionError(str(e))


def _classify_bad_status(e: websocket.WebSocketBadStatusException) -> _errors.AxilioError:
    """Reattach HTTP status is the out-of-band liveness signal: 403 means
    the allocation is no longer active (terminal), 401 a bad token
    (terminal); anything else is transient."""
    status = getattr(e, "status_code", None)
    if status == 403:
        return _errors.SessionEndedError(f"session is no longer active: {e}")
    if status == 401:
        return _errors.UnauthorizedError(f"control token rejected: {e}")
    return _errors.ConnectionError(f"cannot connect to control websocket: {e}")


class _DeadlineWebSocket(websocket.WebSocket):
    """A WebSocket whose socket reads stop at an absolute deadline.

    A socket timeout bounds each underlying read, not the frame. A reply
    that trickles in a few bytes per read would keep ``recv()`` assembling it
    past the caller's deadline. Each read here gets at most the time left
    before ``read_deadline``, so the frame read gives up on time. Its partial
    state stays in the frame buffer, so the next read resumes it.
    """

    read_deadline: float | None = None

    def _recv(self, bufsize: int) -> bytes:
        if self.read_deadline is not None:
            remaining = self.read_deadline - time.monotonic()
            if remaining <= 0:
                raise websocket.WebSocketTimeoutException("read deadline passed")
            self.settimeout(remaining)
        data: bytes = super()._recv(bufsize)
        return data


class _RealWSConn:
    """The production connection: wraps websocket-client so a server close
    frame surfaces as ServerClosed with its code, instead of the empty
    string the high-level ``recv()`` collapses it to."""

    def __init__(self, ws: _DeadlineWebSocket) -> None:
        self._ws = ws

    def settimeout(self, t: float | None) -> None:
        """Bound the next operations to t seconds from now.

        That covers each socket read and the frame as a whole (see
        _DeadlineWebSocket).
        """
        self._ws.settimeout(t)
        self._ws.read_deadline = None if t is None else time.monotonic() + t

    def send(self, text: str) -> None:
        self._ws.send(text)

    def recv(self) -> str:
        while True:
            opcode, data = self._ws.recv_data(control_frame=False)
            if opcode == websocket.ABNF.OPCODE_TEXT:
                return data.decode("utf-8") if isinstance(data, bytes) else str(data)
            if opcode == websocket.ABNF.OPCODE_CLOSE:
                code = int.from_bytes(data[:2], "big") if len(data) >= 2 else None
                reason = data[2:].decode("utf-8", "replace") if len(data) > 2 else ""
                raise ServerClosed(code, reason)
            # Binary / other frames: DCP is text-only; skip.

    def close(self) -> None:
        # The close handshake runs its own wait; a stale call deadline must
        # not cut it short.
        self._ws.read_deadline = None
        self._ws.close()

    def abort(self) -> None:
        """Close the socket at once, without the close handshake."""
        self._ws.shutdown()


def _default_ws_connect(url: str, open_timeout: float) -> _WSConn:
    ws = websocket.create_connection(url, timeout=open_timeout, class_=_DeadlineWebSocket)
    # class_ makes create_connection build that class; its annotation is the base.
    return _RealWSConn(cast(_DeadlineWebSocket, ws))
