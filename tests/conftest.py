"""Test fixtures: a fake Unix-socket daemon that records the DCP
commands it receives and replies with canned responses.

The fake daemon mirrors the Go-side daemon's wire protocol: line-
delimited JSON DCP frames — one ``{"id", "method", "params"}`` command
per request, one ``{"id", "result"|"error"}`` response per reply,
multiple commands per connection. Tests assert against the recorded
commands and configure replies as needed.
"""

from __future__ import annotations

import contextlib
import json
import os
import socket
import threading
from collections.abc import Callable, Iterator
from dataclasses import dataclass, field
from typing import Any

import pytest


@dataclass
class FakeDaemon:
    """A bound Unix-socket listener + accept loop running in a thread.

    Commands received are appended to `received` (under the lock).
    Responses come from `responder` — a callable that takes the
    decoded command frame and returns a response frame. The default
    responder returns `{"id": cmd["id"], "result": {}}` for every
    command; tests override per-test.
    """

    socket_path: str
    received: list[dict[str, Any]] = field(default_factory=list)
    responder: Callable[[dict[str, Any]], dict[str, Any]] | None = None

    _server: socket.socket | None = None
    _thread: threading.Thread | None = None
    _stop: threading.Event = field(default_factory=threading.Event)
    _lock: threading.Lock = field(default_factory=threading.Lock)

    def start(self) -> None:
        if self._server is not None:
            raise RuntimeError("already started")
        srv = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        srv.bind(self.socket_path)
        srv.listen(4)
        srv.settimeout(0.2)
        self._server = srv
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()

    def stop(self) -> None:
        self._stop.set()
        if self._server is not None:
            with contextlib.suppress(OSError):
                self._server.close()
        if self._thread is not None:
            self._thread.join(timeout=2)
        with contextlib.suppress(FileNotFoundError):
            os.remove(self.socket_path)

    def _default_responder(self, cmd: dict[str, Any]) -> dict[str, Any]:
        return {"id": cmd.get("id", 0), "result": {}}

    def _run(self) -> None:
        assert self._server is not None
        while not self._stop.is_set():
            try:
                conn, _ = self._server.accept()
            except TimeoutError:
                continue
            except OSError:
                return
            threading.Thread(target=self._handle_conn, args=(conn,), daemon=True).start()

    def _handle_conn(self, conn: socket.socket) -> None:
        try:
            buf = b""
            with conn:
                while not self._stop.is_set():
                    while b"\n" not in buf:
                        try:
                            chunk = conn.recv(4096)
                        except OSError:
                            return
                        if not chunk:
                            return
                        buf += chunk
                    line, _, buf = buf.partition(b"\n")
                    cmd = json.loads(line.decode("utf-8"))
                    with self._lock:
                        self.received.append(cmd)
                    responder = self.responder or self._default_responder
                    resp = responder(cmd)
                    # A responder may return several frames (e.g. a stale
                    # reply followed by the real one) as a list.
                    frames = resp if isinstance(resp, list) else [resp]
                    for frame in frames:
                        conn.sendall((json.dumps(frame) + "\n").encode("utf-8"))
        except OSError:
            pass


@pytest.fixture
def fake_daemon(tmp_path: Any) -> Iterator[FakeDaemon]:
    socket_path = str(tmp_path / "sdk.sock")
    daemon = FakeDaemon(socket_path=socket_path)
    daemon.start()
    try:
        yield daemon
    finally:
        daemon.stop()
