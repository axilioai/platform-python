"""client.argus wiring (AXI-1108, AXI-2154): argus (vision inference) is a
separately generated Fern client (axilio.argus.ArgusApi) exposed as
client.argus, grouped by the argus 2.0 resources."""

from __future__ import annotations

import json

import pytest

from axilio.argus import AccessibilityTreeNode
from axilio.argus.core.api_error import ApiError as ArgusApiError
from axilio.argus.errors import PaymentRequiredError
from axilio.platform import Client

_ARGUS = "https://argus.axilio.ai"


def test_argus_exposes_the_argus_2_resources() -> None:
    c = Client(api_key="axl_test")
    assert hasattr(c.argus.models, "list_models")
    assert hasattr(c.argus.screenshots, "detect")
    assert hasattr(c.argus.screenshots, "locate")
    assert hasattr(c.argus.accessibility_trees, "accessibility_trees_locate")


def test_argus_base_url_defaults_to_argus_host() -> None:
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
    # since its own paths already carry it.
    c = Client(api_key="axl_test")
    assert c._argus is not c._api


def test_model_catalog_uses_the_models_path(httpx_mock) -> None:  # noqa: ANN001
    httpx_mock.add_response(
        method="GET", url=f"{_ARGUS}/api/v1/models", json={"object": "list", "data": []}
    )
    out = Client(api_key="axl_test", max_retries=0).argus.models.list_models()
    assert out.data == []


def test_tree_locate_wire_shape(httpx_mock) -> None:  # noqa: ANN001
    httpx_mock.add_response(
        method="POST",
        url=f"{_ARGUS}/api/v1/accessibility-trees:locate",
        json={
            "found": True,
            "node_id": "n2",
            "confidence": 0.9,
            "model": "m",
            "cost_microdollars": 10,
            "prompt_tokens": 1,
            "completion_tokens": 1,
            "latency_ms": 5,
        },
    )
    out = Client(
        api_key="axl_test", max_retries=0
    ).argus.accessibility_trees.accessibility_trees_locate(
        query="the log in button",
        nodes=[AccessibilityTreeNode(node_id="n2", role="button", name="Log in")],
    )
    body = json.loads(httpx_mock.get_requests()[0].content)
    assert body["query"] == "the log in button"
    assert body["nodes"][0]["node_id"] == "n2"
    assert out.found is True
    assert out.node_id == "n2"


def test_problem_json_errors_raise_typed_api_errors(httpx_mock) -> None:  # noqa: ANN001
    problem = {
        "type": "about:blank",
        "title": "Payment Required",
        "status": 402,
        "detail": "insufficient balance",
        "code": "payment_required",
    }
    httpx_mock.add_response(
        method="POST",
        url=f"{_ARGUS}/api/v1/screenshots:detect",
        status_code=402,
        headers={"content-type": "application/problem+json"},
        content=json.dumps(problem).encode(),
    )
    with pytest.raises(PaymentRequiredError) as info:
        Client(api_key="axl_test", max_retries=0).argus.screenshots.detect(image="aGk=")
    # argus has its own generated ApiError base, separate from the backend's.
    assert isinstance(info.value, ArgusApiError)
    assert info.value.status_code == 402
    assert info.value.body.detail == "insufficient balance"
    assert info.value.body.code == "payment_required"
