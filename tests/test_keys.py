"""The hand-written named keys must match the contract's enum (AXI-2025).

`keys.Key` is what users press; `_wire.Key` is generated from the contract.
A name present on one side and not the other fails here, so a key the phone
learns cannot reach users only as a raw string.
"""

from __future__ import annotations

from axilio.drivers.mobile import _wire
from axilio.drivers.mobile.keys import Key


def test_named_keys_match_contract() -> None:
    exposed = {v for k, v in vars(Key).items() if k.isupper()}
    contract = {member.value for member in _wire.Key}
    assert contract, "contract has no KeyboardKeyPressParams.key enum"
    assert exposed == contract
