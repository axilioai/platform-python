from __future__ import annotations

import typing

from axilio import PhoneAvailableListResponse
from axilio.phones import PhoneAllocateRequestPhoneType, PhonesAvailableRequestPhoneType


def _literal_values(type_alias: object) -> set[str]:
    values: set[str] = set()
    for member in typing.get_args(type_alias):
        if typing.get_origin(member) is typing.Literal:
            values.update(typing.get_args(member))
    return values


def test_availability_response_is_final_android_only_shape() -> None:
    response = PhoneAvailableListResponse(android_count=0, phones=[])

    model_fields = typing.cast(
        typing.Mapping[str, object],
        getattr(type(response), "model_fields", {}),
    )
    if not model_fields:  # Pydantic v1
        model_fields = typing.cast(
            typing.Mapping[str, object],
            getattr(type(response), "__fields__", {}),
        )
    assert set(model_fields) >= {"android_count", "phones"}
    assert "iphone_count" not in model_fields
    assert response.android_count == 0
    assert response.phones == []


def test_customer_phone_request_literals_are_android_only() -> None:
    assert _literal_values(PhoneAllocateRequestPhoneType) == {"android"}
    assert _literal_values(PhonesAvailableRequestPhoneType) == {"android"}
