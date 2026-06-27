from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="PhoneRentalPhoneRentalUpcomingCharge")


@_attrs_define
class PhoneRentalPhoneRentalUpcomingCharge:
    """
    Attributes:
        amount_cents (int):
        count (int):
        date (datetime.datetime):
    """

    amount_cents: int
    count: int
    date: datetime.datetime

    def to_dict(self) -> dict[str, Any]:
        amount_cents = self.amount_cents

        count = self.count

        date = self.date.isoformat()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "amount_cents": amount_cents,
                "count": count,
                "date": date,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        amount_cents = d.pop("amount_cents")

        count = d.pop("count")

        date = datetime.datetime.fromisoformat(d.pop("date"))

        phone_rental_phone_rental_upcoming_charge = cls(
            amount_cents=amount_cents,
            count=count,
            date=date,
        )

        return phone_rental_phone_rental_upcoming_charge
