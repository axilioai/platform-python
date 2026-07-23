"""File-library convenience: upload local files and push them to phones.

Wraps the generated ``files`` + ``phones`` REST clients with the ergonomics the
raw API doesn't cover:

* ``client.files.upload(path)`` — guess filename/mime/size from a local path,
  register the file, and PUT its bytes to the presigned URL.
* ``client.phones.push_file(phone_id, file_id)`` — push an already-uploaded
  library file to a phone (reuse the same file across phones).
* ``client.phones.send_file(phone_id, path)`` — the one-shot: upload + push,
  optionally waiting for the phone to finish downloading.

Both namespaces delegate every other attribute to the generated client, so
``client.phones.allocate(...)`` etc. keep working unchanged. Hand-written and
preserved across ``fern generate`` via ``src/axilio/.fernignore``.
"""

from __future__ import annotations

import mimetypes
import os
import time
import typing

import httpx

from ..types.file_delivery_summary import FileDeliverySummary
from ..types.file_summary import FileSummary

# Sent when the extension doesn't map to a known type. The backend MIME
# whitelist will reject anything it doesn't accept, so we don't second-guess it
# here beyond a sane default.
_DEFAULT_MIME = "application/octet-stream"

# A delivery is done once the phone reports back (or the push failed); until
# then it is still in flight.
_TERMINAL_STATUSES = frozenset({"delivered", "failed"})


def _file_meta(path: str, filename: str | None, mime_type: str | None) -> tuple[str, str, int]:
    """Derive (filename, mime_type, size_bytes) for a local file."""
    name = filename or os.path.basename(path)
    resolved_mime = mime_type or mimetypes.guess_type(name)[0] or _DEFAULT_MIME
    return name, resolved_mime, os.path.getsize(path)


class _FilesNamespace:
    """``client.files``: the generated files client plus ``upload(path)``."""

    def __init__(self, api: typing.Any) -> None:
        self._api = api

    def __getattr__(self, name: str) -> typing.Any:
        # Delegate create / list / delete (and anything future) to the generated
        # files client, so this wrapper only adds, never hides.
        return getattr(self._api.files, name)

    def upload(
        self,
        path: str,
        *,
        filename: str | None = None,
        mime_type: str | None = None,
    ) -> FileSummary:
        """Register a local file and upload its bytes to the org library.

        Returns the :class:`FileSummary`; its ``.id`` is what
        :meth:`_PhonesNamespace.push_file` / ``send_file`` take. ``filename`` and
        ``mime_type`` default to the basename and a guess from the extension.
        """
        name, resolved_mime, size = _file_meta(path, filename, mime_type)
        registered = self._api.files.create(filename=name, mime_type=resolved_mime, size_bytes=size)
        with open(path, "rb") as handle:
            data = handle.read()
        # The presigned PUT goes straight to object storage: no Axilio auth
        # header, and the Content-Type must match what was registered (the push
        # HeadObject-verifies size + type). httpx sets Content-Length from the
        # body, which matches size_bytes.
        response = httpx.put(
            registered.upload_url,
            content=data,
            headers={"Content-Type": resolved_mime},
            timeout=max(30.0, float(registered.upload_expires_in_seconds)),
        )
        response.raise_for_status()
        return registered.file


class _PhonesNamespace:
    """``client.phones``: the generated phones client plus file-push helpers."""

    def __init__(self, client: typing.Any) -> None:
        self._client = client

    def __getattr__(self, name: str) -> typing.Any:
        # Delegate allocate / deallocate / list_files / push_file (raw) / etc.
        return getattr(self._client.raw.phones, name)

    def push_file(
        self,
        phone_id: str,
        file_id: str,
        *,
        collection: str | None = None,
    ) -> FileDeliverySummary:
        """Push an already-uploaded library file to a phone.

        Returns the :class:`FileDeliverySummary` (status ``dispatched`` once the
        phone acks). ``collection`` overrides the MediaStore bucket (DCIM /
        Pictures / Movies); it defaults by media class server-side.
        """
        return self._client.raw.phones.push_file(phone_id, file_id, collection=collection).delivery

    def send_file(
        self,
        phone_id: str,
        path: str,
        *,
        collection: str | None = None,
        filename: str | None = None,
        mime_type: str | None = None,
        wait: bool = False,
        timeout: float = 60.0,
        poll_interval: float = 2.0,
    ) -> FileDeliverySummary:
        """Upload a local file and push it to a phone in one call.

        Returns the delivery right after dispatch (status ``dispatched``). With
        ``wait=True`` it polls ``list_files`` until the phone reports terminal
        status (``delivered`` / ``failed``) or ``timeout`` seconds elapse,
        returning the latest delivery either way — inspect ``.status`` /
        ``.error``.
        """
        uploaded = self._client.files.upload(path, filename=filename, mime_type=mime_type)
        delivery = self.push_file(phone_id, uploaded.id, collection=collection)
        if not wait:
            return delivery
        return self._await_terminal(phone_id, delivery, timeout, poll_interval)

    def _await_terminal(
        self,
        phone_id: str,
        delivery: FileDeliverySummary,
        timeout: float,
        poll_interval: float,
    ) -> FileDeliverySummary:
        deadline = time.monotonic() + timeout
        while delivery.status not in _TERMINAL_STATUSES and time.monotonic() < deadline:
            time.sleep(poll_interval)
            page = self._client.raw.phones.list_files(phone_id, limit=100)
            for candidate in page.deliveries:
                if candidate.id == delivery.id:
                    delivery = candidate
                    break
        return delivery
