from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="PhoneRentalCreatePhoneRentalCheckoutRequest")


@_attrs_define
class PhoneRentalCreatePhoneRentalCheckoutRequest:
    """
    Attributes:
        plan_id (str):
        schema (str | Unset): A URL to the JSON Schema for this object.
    """

    plan_id: str
    schema: str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        plan_id = self.plan_id

        schema = self.schema

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "plan_id": plan_id,
            }
        )
        if schema is not UNSET:
            field_dict["$schema"] = schema

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        plan_id = d.pop("plan_id")

        schema = d.pop("$schema", UNSET)

        phone_rental_create_phone_rental_checkout_request = cls(
            plan_id=plan_id,
            schema=schema,
        )

        return phone_rental_create_phone_rental_checkout_request
