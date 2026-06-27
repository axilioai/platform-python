from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="PhoneRentalPhoneRentalIntervalSummary")


@_attrs_define
class PhoneRentalPhoneRentalIntervalSummary:
    """
    Attributes:
        count (int):
        interval (str):
        monthly_cents (int):
    """

    count: int
    interval: str
    monthly_cents: int

    def to_dict(self) -> dict[str, Any]:
        count = self.count

        interval = self.interval

        monthly_cents = self.monthly_cents

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "count": count,
                "interval": interval,
                "monthly_cents": monthly_cents,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        count = d.pop("count")

        interval = d.pop("interval")

        monthly_cents = d.pop("monthly_cents")

        phone_rental_phone_rental_interval_summary = cls(
            count=count,
            interval=interval,
            monthly_cents=monthly_cents,
        )

        return phone_rental_phone_rental_interval_summary
