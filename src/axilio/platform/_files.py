"""File-library convenience: upload local files and push them to phones.

Wraps the generated ``uploads`` + ``phones`` REST clients with the ergonomics
the raw API doesn't cover:

* ``client.files.upload(path)`` — guess filename/mime/size from a local path,
  register the file, PUT its bytes to the presigned URL, and complete it.
* ``client.files.list()`` / ``client.files.delete(id)`` — see and clear the
  library, so a caller that can fill the quota can also reclaim it.
* ``client.phones.push_file(phone_id, file_id)`` — send an already-uploaded
  library file to a phone (reuse the same file across phones).
* ``client.phones.send_file(phone_id, path)`` — the one-shot: upload + send,
  optionally waiting for the phone to finish downloading.

Both namespaces delegate every other attribute to the generated client, so
``client.phones.allocate(...)`` etc. keep working unchanged. Hand-written and
preserved across ``fern generate`` via ``src/axilio/.fernignore``.

.. warning::
   Because ``.fernignore`` protects this file, it does NOT move when the
   generated client changes shape — and mypy cannot help, since the generated
   packages are excluded from type checking. A rename on the API side (as in
   the /files -> /uploads move) leaves this file calling methods that no
   longer exist, and nothing fails until a user calls it. ``tests/test_files.py``
   exists to be that failure: it drives every helper here through a mocked
   transport, so a drift breaks CI instead of a customer.
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

# Content type per extension for everything the API's upload whitelist accepts.
# ``mimetypes.guess_type`` is not a safe source here: its built-in table maps
# ``.mkv`` to ``video/matroska`` and ``.3gp`` to ``audio/3gpp``, neither of
# which the server accepts, and whether you get those or the correct values
# depends on whether the host happens to ship an ``/etc/mime.types`` that
# overrides them. Since the API pins Content-Type into the presigned PUT, that
# difference is not cosmetic: the same file uploads fine on a developer laptop
# and is rejected from a slim container.
_EXT_MIME = {
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".png": "image/png",
    ".webp": "image/webp",
    ".gif": "image/gif",
    ".heic": "image/heic",
    ".mp4": "video/mp4",
    ".webm": "video/webm",
    ".mov": "video/quicktime",
    ".3gp": "video/3gpp",
    ".mkv": "video/x-matroska",
}

# A delivery is done once the phone reports back (or the push failed); until
# then it is still in flight.
_TERMINAL_STATUSES = frozenset({"delivered", "failed"})

# The server's per-delivery ceiling: the phone downloads over its own cellular
# link, so the bound belongs to that transport — the library itself stores
# files up to 1 GiB, including files no phone can receive. Mirrored rather
# than fetched, and the server stays authoritative (it rejects an oversize
# push regardless); this constant only lets the one-shot send helpers refuse
# BEFORE uploading a file that could never be delivered, which would otherwise
# be retained in the library by a failed call. Pinned by a backend regression
# test (AXI-1581); the Go twin exports the same number as
# ``files.MaxDeliveryBytes``.
MAX_DELIVERY_BYTES = 100 * 1024 * 1024


class FileTooLargeForDeliveryError(ValueError):
    """A one-shot send was refused before upload: the file exceeds the
    100 MiB phone-delivery limit.

    Raised by :meth:`_PhonesNamespace.send_file` / :meth:`_FilesNamespace.send`
    before any request goes out. A bare :meth:`_FilesNamespace.upload`
    deliberately never raises this — the library accepts what phones cannot
    receive, and upload is the library door.
    """

    def __init__(self, path: str, size_bytes: int) -> None:
        super().__init__(
            f"{os.path.basename(path)} is {size_bytes} bytes; phone delivery is "
            f"limited to {MAX_DELIVERY_BYTES} bytes (100 MiB), so nothing was "
            "uploaded. The org library itself stores files up to 1 GiB — use "
            "upload() and push() separately if you only need it stored"
        )
        self.size_bytes = size_bytes
        self.max_delivery_bytes = MAX_DELIVERY_BYTES


def _detect_mime(name: str) -> str:
    """Resolve a filename to a content type: our table, then the host, then a default."""
    ext = os.path.splitext(name)[1].lower()
    if ext in _EXT_MIME:
        return _EXT_MIME[ext]
    return mimetypes.guess_type(name)[0] or _DEFAULT_MIME


def _file_meta(path: str, filename: str | None, mime_type: str | None) -> tuple[str, str, int]:
    """Derive (filename, mime_type, size_bytes) for a local file."""
    name = filename or os.path.basename(path)
    resolved_mime = mime_type or _detect_mime(name)
    return name, resolved_mime, os.path.getsize(path)


class _FilesNamespace:
    """``client.files``: the generated uploads client plus the file helpers.

    Carries the full vocabulary — upload, push, send, list, delete — so the
    Python and Go surfaces agree. Go exposes all five through ``files``, while
    Python used to split them, with upload/list/delete here and push/send on
    ``client.phones``: the same five operations, reachable under two different
    namespaces depending on which SDK you happened to be reading.

    ``client.phones.push_file`` / ``send_file`` remain, both because they read
    well when the phone is the subject and because removing them would break
    callers for no gain.
    """

    def __init__(self, client: typing.Any) -> None:
        self._client = client
        self._api = client.raw

    def __getattr__(self, name: str) -> typing.Any:
        # Delegate create / list / delete / complete (and anything future) to
        # the generated uploads client, so this wrapper only adds, never hides.
        return getattr(self._api.uploads, name)

    def push(
        self,
        phone_id: str,
        file_id: str,
        *,
        collection: str | None = None,
        wait: bool = False,
        timeout: float = 60.0,
        poll_interval: float = 2.0,
    ) -> FileDeliverySummary:
        """Send an already-uploaded library file to a phone.

        The same call as :meth:`_PhonesNamespace.push_file`, reachable from the
        namespace that owns the file.
        """
        return self._client.phones.push_file(
            phone_id,
            file_id,
            collection=collection,
            wait=wait,
            timeout=timeout,
            poll_interval=poll_interval,
        )

    def send(
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

        The same call as :meth:`_PhonesNamespace.send_file`.
        """
        return self._client.phones.send_file(
            phone_id,
            path,
            collection=collection,
            filename=filename,
            mime_type=mime_type,
            wait=wait,
            timeout=timeout,
            poll_interval=poll_interval,
        )

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
        registered = self._api.uploads.create(
            filename=name, mime_type=resolved_mime, size_bytes=size
        )
        # The presigned PUT goes straight to object storage: no Axilio auth
        # header, and the Content-Type must match what was registered (the
        # signature pins both type and length).
        #
        # The handle is passed rather than its bytes so httpx streams it. The
        # library accepts up to 1 GB per file, and reading that into memory to
        # send it was fine only while the cap was 5 MiB. Content-Length is set
        # explicitly because httpx would otherwise use chunked encoding for a
        # file-like body, which the signature rejects.
        with open(path, "rb") as handle:
            response = httpx.put(
                registered.upload_url,
                content=handle,
                headers={"Content-Type": resolved_mime, "Content-Length": str(size)},
                timeout=max(30.0, float(registered.upload_expires_in_seconds)),
            )
        response.raise_for_status()
        # Completion is what makes the file deliverable: the server verifies the
        # object landed at the declared size and type, checks the content really
        # is the media it claims, and flips the row to ready. Skipping it leaves
        # the file stuck 'uploading' and every send would reject it. Previously
        # the first push verified lazily, which only worked because send_file
        # always pushed — a bare upload() left an unusable file behind.
        completed = self._api.uploads.complete(registered.file.id)
        return completed.file

    def delete(self, upload_id: str) -> None:
        """Remove a file from the library: object, entry and delivery history.

        The other half of a quota: without it a caller can fill a capped
        library through this SDK and has no supported way to clear it.
        """
        self._api.uploads.delete(upload_id)


class _PhonesNamespace:
    """``client.phones``: the generated phones client plus file-push helpers."""

    def __init__(self, client: typing.Any) -> None:
        self._client = client

    def __getattr__(self, name: str) -> typing.Any:
        # Delegate allocate / deallocate / list_deliveries / get_delivery / etc.
        return getattr(self._client.raw.phones, name)

    def push_file(
        self,
        phone_id: str,
        file_id: str,
        *,
        collection: str | None = None,
        wait: bool = False,
        timeout: float = 60.0,
        poll_interval: float = 2.0,
    ) -> FileDeliverySummary:
        """Push an already-uploaded library file to a phone.

        Returns the :class:`FileDeliverySummary` right after dispatch (status
        ``dispatched`` once the phone acks). ``collection`` overrides the
        MediaStore bucket (DCIM / Pictures / Movies); it defaults by media
        class server-side. With ``wait=True`` it polls this delivery until the
        phone reports terminal status (``delivered`` / ``failed``) or
        ``timeout`` seconds elapse, returning the latest delivery either way.

        Waiting used to live only in :meth:`send_file`, which had the split
        backwards: ``send_file`` always uploads first, while this method exists
        for the flow where the file is already in the library and is being
        fanned out to several phones, which is exactly when you want to know
        each one landed. The wait belongs to the delivery, not to how the file
        got into the library.
        """
        delivery = self._client.raw.phones.create_delivery(
            phone_id, file_id=file_id, collection=collection
        ).delivery
        if not wait:
            return delivery
        return self._await_terminal(phone_id, delivery, timeout, poll_interval)

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

        Upload followed by :meth:`push_file`, with every option forwarded, so
        ``wait`` behaves identically here and on a bare push. Returns the
        delivery right after dispatch (status ``dispatched``), or with
        ``wait=True`` the latest delivery once the phone reports terminal
        status or ``timeout`` seconds elapse — inspect ``.status`` /
        ``.error``.

        Raises :class:`FileTooLargeForDeliveryError` before any request goes
        out when the file exceeds the 100 MiB phone-delivery limit (AXI-1581):
        uploading first and letting the delivery refuse would retain the file
        in the library — quota consumed by a failed one-shot call. The check
        lives here and not in :meth:`_FilesNamespace.upload` because only the
        send helpers promise delivery; upload keeps the library's own 1 GiB
        contract.
        """
        size = os.path.getsize(path)
        if size > MAX_DELIVERY_BYTES:
            raise FileTooLargeForDeliveryError(path, size)
        uploaded = self._client.files.upload(path, filename=filename, mime_type=mime_type)
        return self.push_file(
            phone_id,
            uploaded.id,
            collection=collection,
            wait=wait,
            timeout=timeout,
            poll_interval=poll_interval,
        )

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
            # Fetch OUR delivery by id. This used to list the newest 100
            # deliveries and scan for a match, which silently lost the target on
            # a busy phone: once 100 newer pushes landed, the delivery being
            # waited on fell off the page, the loop stopped updating it, and the
            # caller got a stale non-terminal record back — indistinguishable
            # from a timeout. The per-delivery endpoint has no such window.
            delivery = self._client.raw.phones.get_delivery(phone_id, delivery.id)
        return delivery
