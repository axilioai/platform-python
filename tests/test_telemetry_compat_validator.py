from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from types import ModuleType

import pytest


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


@pytest.mark.parametrize(
    ("environment", "base_url"),
    [
        ("staging", "https://api.axilio.ai"),
        ("staging", "https://example.invalid"),
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
