"""client.argus wiring (AXI-1108): argus (vision inference) is a separately
generated Fern client (axilio.argus.ArgusApi) exposed as client.argus."""

from __future__ import annotations

import pytest

from axilio.platform import Client


def test_argus_exposes_vision_methods() -> None:
    c = Client(api_key="axl_test")
    for method in ("detect", "locate", "list_models"):
        assert hasattr(c.argus, method), method


def test_argus_base_url_defaults_to_argus_host() -> None:
    # Argus runs on its own host and its paths already carry /api/v1, so the
    # base URL is the bare host with no prefix appended.
    c = Client(api_key="axl_test")
    assert c._argus_base_url == "https://argus.axilio.ai"
    assert "/api/v1" not in c._argus_base_url


def test_argus_base_url_param_and_env_override(monkeypatch: pytest.MonkeyPatch) -> None:
    c = Client(api_key="axl_test", argus_base_url="https://staging-argus.axilio.ai/")
    assert c._argus_base_url == "https://staging-argus.axilio.ai"

    monkeypatch.setenv("AXILIO_ARGUS_BASE_URL", "https://env-argus.axilio.ai")
    assert Client(api_key="axl_test")._argus_base_url == "https://env-argus.axilio.ai"


def test_argus_is_separate_from_the_backend_client() -> None:
    # The backend client gets /api/v1 folded into its base URL; argus does not,
    # and the two are distinct clients (no auth-header / path collision).
    c = Client(api_key="axl_test")
    assert c._base_url == "https://api.axilio.ai"
    assert c._argus is not c._api
