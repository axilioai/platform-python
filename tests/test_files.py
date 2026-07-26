"""Guard tests for the hand-written file-library convenience layer.

WHY THIS FILE EXISTS
--------------------
``src/axilio/platform/_files.py`` is hand-written but tightly coupled to the
*generated* client, and nothing else in this repo checks that coupling:

* ``.fernignore`` protects ``platform/`` from regen, so the wrapper keeps
  calling whatever it called before even when the generated surface is renamed.
* mypy excludes the generated packages (``src/axilio/phones/`` etc.) and the
  wrapper types its client as ``typing.Any``, so no static check can see
  through to the methods being called.
* Python has no compiler, so a call to a method that no longer exists is a
  runtime ``AttributeError`` — invisible until a user hits it.

That combination bit us once: the ``/files -> /uploads`` API rename regenerated
the client (``phones.push_file`` -> ``phones.create_delivery``,
``phones.list_files`` -> ``phones.list_deliveries``) and this wrapper kept
calling the old names. Every check in CI passed and the package shipped broken.
The equivalent Go SDK caught the same drift instantly, because there the
convenience layer is compiled against the generated client.

These tests are the compiler Python doesn't have. They drive each public helper
through a mocked transport, so if a generated method is renamed, moved, or has
its signature changed, CI fails here instead of a customer finding it.
"""

from __future__ import annotations

import json
import typing

import pytest

from axilio.platform import Client

# The client appends /api/v1 to the configured base URL; these tests assert
# against the full request URL, so _BASE carries the prefix.
_BASE = "https://api.test.invalid/api/v1"
_UPLOAD_URL = "https://storage.test.invalid/put-here"


@pytest.fixture
def client() -> Client:
    return Client(api_key="axl_test", base_url="https://api.test.invalid")


def _file_summary(file_id: str = "file_1", status: str = "ready") -> dict[str, typing.Any]:
    return {
        "id": file_id,
        "filename": "demo.png",
        "mime_type": "image/png",
        "size_bytes": 3,
        "status": status,
        "created_at": "2026-07-26T00:00:00Z",
    }


def _delivery(delivery_id: str = "del_1", status: str = "dispatched") -> dict[str, typing.Any]:
    return {
        "id": delivery_id,
        "file_id": "file_1",
        "phone_id": "phn_1",
        "filename": "demo.png",
        "mime_type": "image/png",
        "size_bytes": 3,
        "status": status,
        "created_at": "2026-07-26T00:00:00Z",
    }


def test_upload_registers_puts_and_completes(client: Client, httpx_mock, tmp_path) -> None:
    """upload() must hit all three steps, in order, on the renamed paths.

    The completion call is the one most likely to be dropped by accident: the
    server used to verify lazily on first push, so an upload that skipped it
    still 'worked' as long as something pushed afterwards. It leaves the file
    stuck 'uploading' otherwise.
    """
    path = tmp_path / "demo.png"
    path.write_bytes(b"abc")

    httpx_mock.add_response(
        method="POST",
        url=f"{_BASE}/uploads",
        json={
            "file": _file_summary(status="uploading"),
            "upload_url": _UPLOAD_URL,
            "upload_expires_in_seconds": 900,
        },
    )
    httpx_mock.add_response(method="PUT", url=_UPLOAD_URL, status_code=200)
    httpx_mock.add_response(
        method="POST",
        url=f"{_BASE}/uploads/file_1/complete",
        json={"file": _file_summary(status="ready")},
    )

    result = client.files.upload(str(path))

    assert result.id == "file_1"
    assert result.status == "ready", "upload() must return the COMPLETED file, not the pending one"

    requests = httpx_mock.get_requests()
    assert [r.method for r in requests] == ["POST", "PUT", "POST"]
    # The presigned PUT must carry the declared content type: the signature
    # pins it, so a mismatch is rejected by storage with an opaque error.
    assert requests[1].headers["Content-Type"] == "image/png"


def test_push_file_uses_the_deliveries_endpoint(client: Client, httpx_mock) -> None:
    httpx_mock.add_response(
        method="POST",
        url=f"{_BASE}/phones/phn_1/deliveries",
        json={"delivery": _delivery()},
    )

    delivery = client.phones.push_file("phn_1", "file_1")

    assert delivery.id == "del_1"
    body = json.loads(httpx_mock.get_requests()[0].content)
    assert (
        body["file_id"] == "file_1"
    ), "the file moved into the request body when the path became delivery-shaped"


def test_send_file_uploads_then_delivers(client: Client, httpx_mock, tmp_path) -> None:
    path = tmp_path / "demo.png"
    path.write_bytes(b"abc")

    httpx_mock.add_response(
        method="POST",
        url=f"{_BASE}/uploads",
        json={
            "file": _file_summary(status="uploading"),
            "upload_url": _UPLOAD_URL,
            "upload_expires_in_seconds": 900,
        },
    )
    httpx_mock.add_response(method="PUT", url=_UPLOAD_URL, status_code=200)
    httpx_mock.add_response(
        method="POST",
        url=f"{_BASE}/uploads/file_1/complete",
        json={"file": _file_summary(status="ready")},
    )
    httpx_mock.add_response(
        method="POST",
        url=f"{_BASE}/phones/phn_1/deliveries",
        json={"delivery": _delivery()},
    )

    delivery = client.phones.send_file("phn_1", str(path))
    assert delivery.status == "dispatched"


def test_send_file_wait_polls_its_own_delivery(client: Client, httpx_mock, tmp_path) -> None:
    """wait=True must fetch THIS delivery by id, not scan a page of the newest.

    The old implementation listed the newest 100 deliveries and looked for a
    match, so on a busy phone the delivery being waited on eventually fell off
    the page and the caller silently got a stale, non-terminal record back.
    Asserting the per-delivery URL is what keeps that from coming back.
    """
    path = tmp_path / "demo.png"
    path.write_bytes(b"abc")

    httpx_mock.add_response(
        method="POST",
        url=f"{_BASE}/uploads",
        json={
            "file": _file_summary(status="uploading"),
            "upload_url": _UPLOAD_URL,
            "upload_expires_in_seconds": 900,
        },
    )
    httpx_mock.add_response(method="PUT", url=_UPLOAD_URL, status_code=200)
    httpx_mock.add_response(
        method="POST",
        url=f"{_BASE}/uploads/file_1/complete",
        json={"file": _file_summary(status="ready")},
    )
    httpx_mock.add_response(
        method="POST",
        url=f"{_BASE}/phones/phn_1/deliveries",
        json={"delivery": _delivery(status="dispatched")},
    )
    httpx_mock.add_response(
        method="GET",
        url=f"{_BASE}/phones/phn_1/deliveries/del_1",
        json=_delivery(status="delivered"),
    )

    delivery = client.phones.send_file(
        "phn_1", str(path), wait=True, timeout=5.0, poll_interval=0.01
    )

    assert delivery.status == "delivered"
    assert any(
        r.method == "GET" and r.url.path.endswith("/phones/phn_1/deliveries/del_1")
        for r in httpx_mock.get_requests()
    ), "the wait loop must read the delivery by id"


def test_push_file_wait_polls_its_own_delivery(client: Client, httpx_mock) -> None:
    """push_file(wait=True) must poll, not return at dispatch.

    Waiting used to exist only on send_file, which had the split backwards:
    push_file is the fan-out verb (one stored file to many phones) and fan-out
    is exactly when confirmation matters. The option was accepted and dropped,
    which no type checker or import-time check can catch.
    """
    httpx_mock.add_response(
        method="POST",
        url=f"{_BASE}/phones/phn_1/deliveries",
        json={"delivery": _delivery(status="dispatched")},
    )
    httpx_mock.add_response(
        method="GET",
        url=f"{_BASE}/phones/phn_1/deliveries/del_1",
        json=_delivery(status="delivered"),
    )

    delivery = client.phones.push_file(
        "phn_1", "file_1", wait=True, timeout=5.0, poll_interval=0.01
    )

    assert delivery.status == "delivered", "wait=True was ignored by push_file"
    assert any(
        r.method == "GET" and r.url.path.endswith("/phones/phn_1/deliveries/del_1")
        for r in httpx_mock.get_requests()
    ), "the wait loop must read the delivery by id"


def test_push_file_without_wait_returns_at_dispatch(client: Client, httpx_mock) -> None:
    httpx_mock.add_response(
        method="POST",
        url=f"{_BASE}/phones/phn_1/deliveries",
        json={"delivery": _delivery(status="dispatched")},
    )

    delivery = client.phones.push_file("phn_1", "file_1")

    assert delivery.status == "dispatched"
    assert not [
        r for r in httpx_mock.get_requests() if r.method == "GET"
    ], "a bare push must not poll"


def test_list_and_delete_reach_the_uploads_endpoints(client: Client, httpx_mock) -> None:
    """The management half of the quota: fillable implies clearable."""
    httpx_mock.add_response(
        method="GET",
        url=f"{_BASE}/uploads?limit=50",
        json={
            "files": [_file_summary()],
            "total": 1,
            "usage": {
                "file_count": 1,
                "file_limit": 10000,
                "total_bytes": 3,
                "byte_limit": 53687091200,
            },
        },
    )
    page = client.files.list(limit=50)
    assert page.total == 1
    assert (
        page.usage.byte_limit == 53687091200
    ), "usage must ride the listing so callers can show X of Y"

    httpx_mock.add_response(
        method="DELETE",
        url=f"{_BASE}/uploads/file_1",
        json={"message": "file deleted successfully"},
    )
    client.files.delete("file_1")
    assert httpx_mock.get_requests()[-1].method == "DELETE"


def test_wrapper_targets_exist_on_the_generated_client(client: Client) -> None:
    """The cheap, direct drift check: every generated method this wrapper calls.

    The behavioural tests above cover these too, but this one names them, so a
    failure reads as 'the generated client no longer has X' rather than an
    AttributeError buried in a request flow.
    """
    for attr in ("create", "complete", "delete", "list"):
        assert hasattr(client.raw.uploads, attr), f"generated uploads client lost .{attr}()"
    for attr in ("create_delivery", "get_delivery", "list_deliveries"):
        assert hasattr(client.raw.phones, attr), f"generated phones client lost .{attr}()"
