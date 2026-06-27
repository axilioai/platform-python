from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="SubscriptionBalanceResponse")


@_attrs_define
class SubscriptionBalanceResponse:
    """
    Attributes:
        balance_display (str):
        balance_microdollars (int):
        schema (str | Unset): A URL to the JSON Schema for this object.
    """

    balance_display: str
    balance_microdollars: int
    schema: str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        balance_display = self.balance_display

        balance_microdollars = self.balance_microdollars

        schema = self.schema

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "balance_display": balance_display,
                "balance_microdollars": balance_microdollars,
            }
        )
        if schema is not UNSET:
            field_dict["$schema"] = schema

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        balance_display = d.pop("balance_display")

        balance_microdollars = d.pop("balance_microdollars")

        schema = d.pop("$schema", UNSET)

        subscription_balance_response = cls(
            balance_display=balance_display,
            balance_microdollars=balance_microdollars,
            schema=schema,
        )

        return subscription_balance_response
