"""The generated DCP wire layer must match the vendored contract.

This is the SDK-side end of the DCP honesty chain: the backend's drift gate
forces the contract to equal the deployed Go server, and this test forces the
generated `_wire` module to equal the contract. Together they guarantee the
SDK's typed layer equals what the server actually speaks. It checks the
generator's *output* against the contract (no codegen at test time), so it runs
with nothing but PyYAML.
"""

from __future__ import annotations

import dataclasses
import pathlib

import yaml

from axilio.drivers.mobile import _wire

CONTRACT = pathlib.Path(__file__).resolve().parent.parent / "contracts" / "dcp-asyncapi.yaml"


def _contract() -> dict:
    return yaml.safe_load(CONTRACT.read_text())


def _wire_consts(prefix: str) -> dict[str, str]:
    return {k: v for k, v in vars(_wire).items() if k.startswith(prefix)}


def test_command_methods_match_contract() -> None:
    doc = _contract()
    want = {
        m["name"] if isinstance(m, dict) and "name" in m else name
        for name, m in doc["components"]["messages"].items()
        if m.get("x-dcp-kind") == "command"
    }
    got = set(_wire_consts("METHOD_").values())
    assert got == want, f"METHOD_* {got} != contract commands {want}"


def test_error_specs_match_contract() -> None:
    doc = _contract()
    want = {k: (s["code"], bool(s["retryable"])) for k, s in doc["x-dcp-error-table"].items()}
    assert want == _wire.ERROR_SPECS
    # Every kind also has a KIND_* constant.
    assert set(_wire_consts("KIND_").values()) == set(want)


def test_protocol_version_matches_contract() -> None:
    assert _contract()["info"]["x-dcp-protocol-version"] == _wire.PROTOCOL_VERSION


def test_every_schema_has_a_dataclass() -> None:
    doc = _contract()
    for schema_name in doc["components"]["schemas"]:
        model = getattr(_wire, schema_name, None)
        assert model is not None and dataclasses.is_dataclass(model), (
            f"contract schema {schema_name} has no generated dataclass in _wire"
        )
