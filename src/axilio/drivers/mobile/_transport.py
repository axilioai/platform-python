"""Transport seam + the in-sandbox SandboxTransport."""

from __future__ import annotations

import contextlib
import json
import os
import socket
import threading
from typing import Any, Protocol, runtime_checkable

import websocket  # websocket-client: synchronous WS client for RemoteTransport

from . import _errors

_DEFAULT_SOCKET_PATH = "/run/axilio/sdk.sock"
_ENV_SOCKET_PATH = "AXILIO_SDK_SOCKET"


@runtime_checkable
class Transport(Protocol):
    """The seam every driver call goes through. One round-trip per call.

    ``method`` is a DCP method name ("Domain.method", e.g. "Input.tap",
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
        try:
            sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
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


# A WS connection only needs send / recv / settimeout / close for the
# transport; the alias documents that and lets tests inject a fake.
_WSConn = Any


class RemoteTransport:
    """`Transport` over the DCP control WebSocket — literal CDP frames.

    The driver already speaks DCP method names, so this transport does no
    name translation: each call goes out as a CDP request
    ``{"id", "method", "params"}`` and the matching ``{"id", "result"|"error"}``
    comes back — the same wire an off-the-shelf CDP client speaks. One
    WebSocket per allocation; reconnect happens lazily on the next call
    after a drop (the allocation lease outlives the socket).
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
        # Injectable connection factory (url, open_timeout) -> conn, for
        # tests; production opens a real WebSocket lazily on first call.
        self._connect = connect or _default_ws_connect

    def call(
        self,
        method: str,
        args: dict[str, Any] | None = None,
        *,
        timeout: float | None = None,
    ) -> dict[str, Any] | None:
        """Send a CDP command, await the id-matched reply, return its result."""
        with self._lock:
            conn = self._ensure_connected()
            self._next_id += 1
            req_id = self._next_id
            frame = _build_frame(req_id, method, args)
            try:
                if timeout is not None:
                    conn.settimeout(timeout)
                conn.send(json.dumps(frame))
                return self._await_reply(conn, req_id)
            except websocket.WebSocketTimeoutException as e:
                self._close_locked()
                raise _errors.TimeoutError(f"{method} timed out after {timeout}s") from e
            except (websocket.WebSocketException, OSError) as e:
                self._close_locked()
                raise _errors.ConnectionError(f"control websocket I/O failed: {e}") from e
            finally:
                if self._conn is not None and timeout is not None:
                    with contextlib.suppress(Exception):
                        conn.settimeout(None)

    def close(self) -> None:
        """Close the underlying WebSocket. Idempotent."""
        with self._lock:
            self._close_locked()

    def _await_reply(self, conn: _WSConn, req_id: int) -> dict[str, Any] | None:
        # Read until the frame that echoes our id. Notifications (events —
        # no id) and any stale frames are skipped: P0 is request/response,
        # and the telemetry up-channel (P1) routes notifications separately.
        while True:
            raw = conn.recv()
            if not raw:
                raise websocket.WebSocketConnectionClosedException("control websocket closed")
            text = raw if isinstance(raw, str) else raw.decode("utf-8")
            msg = _decode_frame(text)
            if msg.get("id") != req_id:
                continue
            return _unwrap_reply(msg)

    def _ensure_connected(self) -> _WSConn:
        if self._conn is None:
            try:
                self._conn = self._connect(self._url, self._open_timeout)
            except (websocket.WebSocketException, OSError) as e:
                raise _errors.ConnectionError(f"cannot connect to control websocket: {e}") from e
        return self._conn

    def _close_locked(self) -> None:
        if self._conn is not None:
            with contextlib.suppress(Exception):
                self._conn.close()
            self._conn = None


def _default_ws_connect(url: str, open_timeout: float) -> _WSConn:
    return websocket.create_connection(url, timeout=open_timeout)
