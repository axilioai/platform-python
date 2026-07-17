"""Smoke tests for the top-level Client. Covers construction, env-var
auth, base-URL handling, mode detection, and the auth header on
outgoing requests. Resource-method tests land alongside each resource
as the typed methods get wired up.
"""

from __future__ import annotations

import pytest

from axilio._mode import Mode
from axilio.platform import Client


def test_client_requires_api_key(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("AXILIO_API_KEY", raising=False)
    monkeypatch.delenv("AXILIO_SANDBOX_TOKEN", raising=False)
    monkeypatch.delenv("AXILIO_ATLAS_ENDPOINT", raising=False)
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


def test_mode_is_local_without_sandbox_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("AXILIO_SANDBOX_TOKEN", raising=False)
    monkeypatch.delenv("AXILIO_ATLAS_ENDPOINT", raising=False)
    with Client(api_key="ax_test") as client:
        assert client.mode is Mode.LOCAL


def test_mode_is_sandbox_with_both_env_vars(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("AXILIO_SANDBOX_TOKEN", "sandbox_tok_test")
    monkeypatch.setenv("AXILIO_ATLAS_ENDPOINT", "10.0.0.1:9092")
    # Pass api_key explicitly so the sandbox-token fallback path runs.
    with Client(api_key="ax_test") as client:
        assert client.mode is Mode.SANDBOX


def test_mode_falls_back_to_local_with_only_one_sandbox_var(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    # Only the token, no endpoint var — treat as misconfiguration.
    monkeypatch.setenv("AXILIO_SANDBOX_TOKEN", "sandbox_tok_test")
    monkeypatch.delenv("AXILIO_ATLAS_ENDPOINT", raising=False)
    with Client(api_key="ax_test") as client:
        assert client.mode is Mode.LOCAL


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
