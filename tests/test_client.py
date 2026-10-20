"""Smoke tests for the top-level Client. Covers construction, env-var
auth, base-URL handling, mode detection, and the auth header on
outgoing requests. Resource-method tests land alongside each resource
as the typed methods get wired up.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from axilio._mode import Mode
from axilio.platform import Client


def _outside_sandbox(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    monkeypatch.setenv("AXILIO_SDK_SOCKET", str(tmp_path / "absent.sock"))


def _inside_sandbox(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    sock = tmp_path / "sdk.sock"
    sock.touch()
    monkeypatch.setenv("AXILIO_SDK_SOCKET", str(sock))


def test_client_requires_api_key(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    monkeypatch.delenv("AXILIO_API_KEY", raising=False)
    _outside_sandbox(monkeypatch, tmp_path)
    with pytest.raises(ValueError, match="API key not provided"):
        Client()


def test_client_reads_env_var(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("AXILIO_API_KEY", "ax_test_from_env")
    client = Client()
    try:
        assert client.api_key == "ax_test_from_env"
    finally:
        client.close()


def test_client_kwarg_overrides_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("AXILIO_API_KEY", "ax_env")
    client = Client(api_key="ax_explicit")
    try:
        assert client.api_key == "ax_explicit"
    finally:
        client.close()


def test_client_default_base_url() -> None:
    client = Client(api_key="ax_test")
    try:
        assert client.base_url == "https://api.axilio.ai"
    finally:
        client.close()


def test_client_base_url_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("AXILIO_BASE_URL", "https://staging-api.axilio.ai/")
    client = Client(api_key="ax_test")
    try:
        # Trailing slash stripped.
        assert client.base_url == "https://staging-api.axilio.ai"
    finally:
        client.close()


def test_client_base_url_kwarg_overrides_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("AXILIO_BASE_URL", "https://staging-api.axilio.ai")
    client = Client(api_key="ax_test", base_url="https://custom.example/")
    try:
        assert client.base_url == "https://custom.example"
    finally:
        client.close()


def test_client_works_as_context_manager() -> None:
    with Client(api_key="ax_test") as client:
        assert client.api_key == "ax_test"
    # __exit__ closed the underlying http client; calling close again is fine.
    client.close()


def test_mode_is_local_without_the_sandbox_socket(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    _outside_sandbox(monkeypatch, tmp_path)
    with Client(api_key="ax_test") as client:
        assert client.mode is Mode.LOCAL


def test_mode_is_sandbox_when_the_sandbox_socket_exists(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    # The sandbox provides its SDK socket and no environment variable, so the
    # socket alone has to switch the client over (AXI-2377).
    _inside_sandbox(monkeypatch, tmp_path)
    with Client(api_key="ax_test") as client:
        assert client.mode is Mode.SANDBOX


def test_sandbox_client_needs_no_api_key(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    # A script written locally as Client() + client.session() must run as a
    # workflow, where no API key is set: session() uses the socket, not the API.
    monkeypatch.delenv("AXILIO_API_KEY", raising=False)
    _inside_sandbox(monkeypatch, tmp_path)
    with Client() as client:
        assert client.mode is Mode.SANDBOX


def test_resources_attached() -> None:
    """Every resource group hangs off the client, delegated to the
    Fern-generated AxilioApi (lazily constructed on first access)."""
    with Client(api_key="ax_test") as client:
        assert client.billing is not None
        assert client.usage is not None
        assert client.api_keys is not None
        assert client.mobile is not None
        assert client.workflows is not None
        assert client.runs is not None
        assert client.webhooks is client.raw.webhooks


def test_account_management_is_not_exposed() -> None:
    """Org and user account management are deliberately absent from the SDK
    (AXI-1124): that surface belongs to the dashboard, not the client. The
    backend still serves the endpoints; we just don't expose them here."""
    with Client(api_key="ax_test") as client:
        assert not hasattr(client, "org")
        assert not hasattr(client, "user")


def test_auth_uses_api_key_header() -> None:
    """Customer auth is the X-Axilio-Api-Key header (the spec's apiKeyAuth
    scheme), not a bearer token. The generated client wrapper builds the
    outgoing headers; assert the key lands there and that we don't also
    emit an Authorization bearer header (that scheme is for user JWTs)."""
    client = Client(api_key="ax_unit", base_url="https://api.example")
    try:
        headers = (
            client.raw._client_wrapper.get_headers()
        )  # noqa: SLF001 — testing the wire contract
        assert headers["X-Axilio-Api-Key"] == "ax_unit"
        assert "Authorization" not in headers
    finally:
        client.close()
