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
    """Every resource class from the design doc hangs off the client."""
    with Client(api_key="ax_test") as client:
        # Smoke test — just verifying the attribute exists and is the
        # right class. Method bodies are stubs until codegen.
        assert client.billing is not None
        assert client.usage is not None
        assert client.api_keys is not None
        assert client.org is not None
        assert client.mobile is not None
        assert client.workflows is not None
        assert client.runs is not None


def test_auth_header_sent(httpx_mock) -> None:
    """The Bearer token must land on the wire."""
    httpx_mock.add_response(json={"ok": True})
    client = Client(api_key="ax_unit", base_url="https://api.example")
    try:
        client._http.get("/v1/health")  # noqa: SLF001 — testing the wire
        request = httpx_mock.get_request()
        assert request.headers["Authorization"] == "Bearer ax_unit"
        assert request.headers["Accept"] == "application/json"
    finally:
        client.close()
