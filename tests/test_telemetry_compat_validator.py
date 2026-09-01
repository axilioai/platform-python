from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
from pathlib import Path
from types import ModuleType

import pytest

from axilio.platform import ApiError


def _load_validator() -> ModuleType:
    path = Path(__file__).parents[1] / "scripts" / "validate_telemetry_compat.py"
    spec = importlib.util.spec_from_file_location("validate_telemetry_compat", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_capture_replay_matrix_passes_with_candidate_sdk() -> None:
    validator = _load_validator()
    recorder = validator.Recorder()

    validator.run_replay(recorder)

    assert recorder.passed
    assert [result.id for result in recorder.results] == [
        "REPLAY-01",
        "REPLAY-02",
        "REPLAY-03",
        "REPLAY-04",
        "REPLAY-05",
        "REPLAY-06",
        "REPLAY-07",
        "REPLAY-08",
    ]


def test_failure_evidence_redacts_exception_details() -> None:
    validator = _load_validator()
    recorder = validator.Recorder()

    def fail() -> str:
        raise RuntimeError("GET /sessions/secret-id Authorization: secret-token")

    recorder.check("TEST-FAIL", "safe failure evidence", fail)

    assert not recorder.passed
    observed = recorder.results[0].observed_redacted
    assert "secret-id" not in observed
    assert "secret-token" not in observed
    assert "error_type=RuntimeError" in observed
    assert "fingerprint=" in observed
    assert "details" not in observed


@pytest.mark.parametrize(
    ("environment", "base_url"),
    [
        ("staging", "https://api.axilio.ai"),
        ("dev", "https://api.axilio.ai."),
        ("staging", "https://example.invalid"),
        ("dev", "https://example.invalid"),
        ("dev", "http://example.invalid"),
        ("production", "https://api.axilio.ai"),
    ],
)
def test_target_guard_refuses_non_dev_staging_origins(environment: str, base_url: str) -> None:
    validator = _load_validator()

    with pytest.raises(ValueError):
        validator._validate_target(environment, base_url)


def test_target_guard_allows_loopback_dev_and_exact_staging() -> None:
    validator = _load_validator()

    assert validator._validate_target("dev", "http://127.0.0.1:8000") == "http://127.0.0.1:8000"
    assert (
        validator._validate_target("staging", "https://staging-api.axilio.ai/")
        == "https://staging-api.axilio.ai"
    )


def test_target_guard_allows_only_separately_approved_remote_dev_origin() -> None:
    validator = _load_validator()
    approved = "https://dev-api.example.invalid"

    assert validator._validate_target("dev", approved, approved) == approved
    with pytest.raises(ValueError):
        validator._validate_target("dev", approved, "https://other-dev.example.invalid")


def test_probe_client_refuses_redirects_before_reusing_credentials() -> None:
    validator = _load_validator()

    with validator.ReplayServer() as base_url:
        client = validator.Client(
            api_key="axl_loopback",
            base_url=base_url,
            timeout=5.0,
            max_retries=0,
            follow_redirects=False,
        )
        with pytest.raises(ApiError) as exc_info:
            client.raw.runs.sessions_list_frames("redirect")
        assert exc_info.value.status_code == 302


def test_results_include_fixture_and_file_provenance(tmp_path: Path) -> None:
    validator = _load_validator()
    recorder = validator.Recorder()
    recorder.check("TEST-PASS", "provenance is complete", lambda: "complete")
    output = tmp_path / "python-pydantic-2.json"

    validator.write_results(
        output,
        recorder,
        environment="staging",
        sdk_ref="candidate-sha",
        artifact_sha256="artifact-sha",
        seed_revision="seed-sha",
        fixture_manifest_sha256="fixture-sha",
    )

    payload = json.loads(output.read_text(encoding="utf-8"))
    assert payload["seed_revision"] == "seed-sha"
    assert payload["fixture_manifest_sha256"] == "fixture-sha"
    assert payload["results"][0]["evidence_file"] == output.name


def test_load_manifest_hashes_exact_consumed_bytes(tmp_path: Path) -> None:
    validator = _load_validator()
    path = tmp_path / "fixtures.json"
    body = json.dumps(
        {
            "manifest_version": 1,
            "environment": "staging",
            "seed_revision": "seed-sha",
            "fixtures": {
                "normal_session": {"id": "normal"},
                "normal_empty_session": {"id": "empty"},
                "expired_session": {"id": "expired"},
            },
        },
        indent=2,
    ).encode()
    path.write_bytes(body)

    manifest, digest = validator._load_manifest(path, "staging")

    assert manifest["seed_revision"] == "seed-sha"
    assert digest == hashlib.sha256(body).hexdigest()
