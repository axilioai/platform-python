"""Transport seam + the in-sandbox SandboxTransport."""

from __future__ import annotations

import contextlib
import json
import os
import socket
import threading
import uuid
from typing import Any, Protocol, runtime_checkable

import websocket  # websocket-client: synchronous WS client for RemoteTransport

from . import _envelope, _errors

_DEFAULT_SOCKET_PATH = "/run/axilio/sdk.sock"
_ENV_SOCKET_PATH = "AXILIO_SDK_SOCKET"


@runtime_checkable
class Transport(Protocol):
    """The seam every driver call goes through. One round-trip per call.

    ``method`` is a DCP method name ("Domain.method", e.g. "Input.tap",
    "Screen.observe") — the driver's helpers translate their ergonomic API
    to these, the same way Playwright's helpers translate to CDP. Transports
    speak the method directly (RemoteTransport) or bridge it to the legacy
    daemon op (SandboxTransport).
    """

    def call(
        self,
        method: str,
        args: dict[str, Any] | None = None,
        *,
        timeout: float | None = None,
    ) -> dict[str, Any] | None: ...

    def close(self) -> None: ...


class SandboxTransport:
    """`Transport` over the in-VM daemon's Unix socket."""

    def __init__(self, socket_path: str | None = None) -> None:
        self._socket_path: str = (
            socket_path or os.environ.get(_ENV_SOCKET_PATH) or _DEFAULT_SOCKET_PATH
        )
        self._lock = threading.Lock()
        self._sock: socket.socket | None = None
        self._buf = b""

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
        """Send a Command, wait for the matching Response, return the decoded result."""
        # Bridge the DCP method to the in-VM daemon's legacy snake-case op
        # until the daemon speaks DCP itself; params + result shapes already
        # match, so only the name is translated. An unmapped method passes
        # through and the daemon rejects it as unknown_op.
        op = _envelope.METHOD_TO_OP.get(method, method)
        cmd = _envelope.Command(id=str(uuid.uuid4()), op=op, args=args)
        with self._lock:
            self._ensure_connected()
            assert self._sock is not None
            try:
                if timeout is not None:
                    self._sock.settimeout(timeout)
                self._send(cmd)
                resp = self._recv()
            except TimeoutError as e:
                self._close_locked()
                raise _errors.TimeoutError(f"{op} timed out after {timeout}s") from e
            except OSError as e:
                self._close_locked()
                raise _errors.ConnectionError(f"socket I/O failed: {e}") from e
            finally:
                if self._sock is not None and timeout is not None:
                    with contextlib.suppress(OSError):
                        self._sock.settimeout(None)
        if resp.id != cmd.id:
            raise _errors.InternalError(f"id mismatch: sent {cmd.id!r}, got {resp.id!r}")
        if not resp.ok:
            if resp.error is None:
                raise _errors.InternalError("daemon returned ok=false with no error body")
            raise _errors.from_wire(resp.error)
        return resp.result

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

    def _send(self, cmd: _envelope.Command) -> None:
        assert self._sock is not None
        line = (json.dumps(cmd.to_wire()) + "\n").encode("utf-8")
        self._sock.sendall(line)

    def _recv(self) -> _envelope.Response:
        assert self._sock is not None
        while b"\n" not in self._buf:
            chunk = self._sock.recv(4096)
            if not chunk:
                raise OSError("daemon closed the connection")
            self._buf += chunk
        line, _, rest = self._buf.partition(b"\n")
        self._buf = rest
        try:
            data = json.loads(line.decode("utf-8"))
        except json.JSONDecodeError as e:
            raise _errors.InternalError(f"daemon sent malformed JSON: {e}") from e
        return _envelope.Response.from_wire(data)


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
            frame: dict[str, Any] = {"id": req_id, "method": method}
            if args is not None:
                frame["params"] = args
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
            try:
                msg = json.loads(text)
            except json.JSONDecodeError as e:
                raise _errors.InternalError(f"control sent malformed JSON: {e}") from e
            if msg.get("id") != req_id:
                continue
            error = msg.get("error")
            if error is not None:
                raise _errors.from_dcp_error(error)
            return msg.get("result")

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
