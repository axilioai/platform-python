from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="SubscriptionDowngradeResponse")


@_attrs_define
class SubscriptionDowngradeResponse:
    """
    Attributes:
        effective_date (datetime.datetime):
        message (str):
        proration_amount (float):
        schema (str | Unset): A URL to the JSON Schema for this object.
    """

    effective_date: datetime.datetime
    message: str
    proration_amount: float
    schema: str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        effective_date = self.effective_date.isoformat()

        message = self.message

        proration_amount = self.proration_amount

        schema = self.schema

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "effective_date": effective_date,
                "message": message,
                "proration_amount": proration_amount,
            }
        )
        if schema is not UNSET:
            field_dict["$schema"] = schema

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        effective_date = datetime.datetime.fromisoformat(d.pop("effective_date"))

        message = d.pop("message")

        proration_amount = d.pop("proration_amount")

        schema = d.pop("$schema", UNSET)

        subscription_downgrade_response = cls(
            effective_date=effective_date,
            message=message,
            proration_amount=proration_amount,
            schema=schema,
        )

        return subscription_downgrade_response
