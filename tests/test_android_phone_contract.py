from __future__ import annotations

import typing

from axilio.phones import PhoneAllocateRequestPhoneType

# The customer availability endpoint (GET /phones/available) and its
# PhoneAvailableListResponse were removed in the 0.72 API (dual-routing
# removal, AXI-1772), so the old android-only availability-shape assertion no
# longer has a surface to test. The android-only invariant now lives on the
# allocate request enum, which this guards.


def _literal_values(type_alias: object) -> set[str]:
    values: set[str] = set()
    for member in typing.get_args(type_alias):
        if typing.get_origin(member) is typing.Literal:
            values.update(typing.get_args(member))
    return values


def test_customer_phone_request_literals_are_android_only() -> None:
    assert _literal_values(PhoneAllocateRequestPhoneType) == {"android"}
