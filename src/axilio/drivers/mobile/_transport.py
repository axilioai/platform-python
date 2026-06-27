"""Transport seam + the in-sandbox SandboxTransport."""

from __future__ import annotations

import contextlib
import json
import os
import socket
import threading
import uuid
from typing import Any, Protocol, runtime_checkable

from . import _envelope, _errors

_DEFAULT_SOCKET_PATH = "/run/axilio/sdk.sock"
_ENV_SOCKET_PATH = "AXILIO_SDK_SOCKET"


@runtime_checkable
class Transport(Protocol):
    """The seam every driver call goes through. One round-trip per call."""

    def call(
        self,
        op: str,
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
        op: str,
        args: dict[str, Any] | None = None,
        *,
        timeout: float | None = None,
    ) -> dict[str, Any] | None:
        """Send a Command, wait for the matching Response, return the decoded result."""
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
