from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="SubscriptionAddFundsRequest")


@_attrs_define
class SubscriptionAddFundsRequest:
    """
    Attributes:
        amount_cents (int):
        schema (str | Unset): A URL to the JSON Schema for this object.
    """

    amount_cents: int
    schema: str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        amount_cents = self.amount_cents

        schema = self.schema

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "amount_cents": amount_cents,
            }
        )
        if schema is not UNSET:
            field_dict["$schema"] = schema

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        amount_cents = d.pop("amount_cents")

        schema = d.pop("$schema", UNSET)

        subscription_add_funds_request = cls(
            amount_cents=amount_cents,
            schema=schema,
        )

        return subscription_add_funds_request
