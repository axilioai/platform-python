from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="PhoneRentalCreatePhoneRentalCheckoutResponse")


@_attrs_define
class PhoneRentalCreatePhoneRentalCheckoutResponse:
    """
    Attributes:
        checkout_url (str):
        schema (str | Unset): A URL to the JSON Schema for this object.
    """

    checkout_url: str
    schema: str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        checkout_url = self.checkout_url

        schema = self.schema

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "checkout_url": checkout_url,
            }
        )
        if schema is not UNSET:
            field_dict["$schema"] = schema

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        checkout_url = d.pop("checkout_url")

        schema = d.pop("$schema", UNSET)

        phone_rental_create_phone_rental_checkout_response = cls(
            checkout_url=checkout_url,
            schema=schema,
        )

        return phone_rental_create_phone_rental_checkout_response
