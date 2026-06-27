from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.phone_rental_phone_rental_interval_summary import PhoneRentalPhoneRentalIntervalSummary
    from ..models.phone_rental_phone_rental_upcoming_charge import PhoneRentalPhoneRentalUpcomingCharge


T = TypeVar("T", bound="PhoneRentalPhoneRentalSummary")


@_attrs_define
class PhoneRentalPhoneRentalSummary:
    """
    Attributes:
        active_count (int):
        combined_monthly_cents (int):
        per_interval (list[PhoneRentalPhoneRentalIntervalSummary] | None):
        upcoming_charges (list[PhoneRentalPhoneRentalUpcomingCharge] | None):
    """

    active_count: int
    combined_monthly_cents: int
    per_interval: list[PhoneRentalPhoneRentalIntervalSummary] | None
    upcoming_charges: list[PhoneRentalPhoneRentalUpcomingCharge] | None

    def to_dict(self) -> dict[str, Any]:
        active_count = self.active_count

        combined_monthly_cents = self.combined_monthly_cents

        per_interval: list[dict[str, Any]] | None
        if isinstance(self.per_interval, list):
            per_interval = []
            for per_interval_type_0_item_data in self.per_interval:
                per_interval_type_0_item = per_interval_type_0_item_data.to_dict()
                per_interval.append(per_interval_type_0_item)

        else:
            per_interval = self.per_interval

        upcoming_charges: list[dict[str, Any]] | None
        if isinstance(self.upcoming_charges, list):
            upcoming_charges = []
            for upcoming_charges_type_0_item_data in self.upcoming_charges:
                upcoming_charges_type_0_item = upcoming_charges_type_0_item_data.to_dict()
                upcoming_charges.append(upcoming_charges_type_0_item)

        else:
            upcoming_charges = self.upcoming_charges

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "active_count": active_count,
                "combined_monthly_cents": combined_monthly_cents,
                "per_interval": per_interval,
                "upcoming_charges": upcoming_charges,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.phone_rental_phone_rental_interval_summary import PhoneRentalPhoneRentalIntervalSummary
        from ..models.phone_rental_phone_rental_upcoming_charge import PhoneRentalPhoneRentalUpcomingCharge

        d = dict(src_dict)
        active_count = d.pop("active_count")

        combined_monthly_cents = d.pop("combined_monthly_cents")

        def _parse_per_interval(data: object) -> list[PhoneRentalPhoneRentalIntervalSummary] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                per_interval_type_0 = []
                _per_interval_type_0 = data
                for per_interval_type_0_item_data in _per_interval_type_0:
                    per_interval_type_0_item = PhoneRentalPhoneRentalIntervalSummary.from_dict(
                        per_interval_type_0_item_data
                    )

                    per_interval_type_0.append(per_interval_type_0_item)

                return per_interval_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[PhoneRentalPhoneRentalIntervalSummary] | None, data)

        per_interval = _parse_per_interval(d.pop("per_interval"))

        def _parse_upcoming_charges(data: object) -> list[PhoneRentalPhoneRentalUpcomingCharge] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                upcoming_charges_type_0 = []
                _upcoming_charges_type_0 = data
                for upcoming_charges_type_0_item_data in _upcoming_charges_type_0:
                    upcoming_charges_type_0_item = PhoneRentalPhoneRentalUpcomingCharge.from_dict(
                        upcoming_charges_type_0_item_data
                    )

                    upcoming_charges_type_0.append(upcoming_charges_type_0_item)

                return upcoming_charges_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[PhoneRentalPhoneRentalUpcomingCharge] | None, data)

        upcoming_charges = _parse_upcoming_charges(d.pop("upcoming_charges"))

        phone_rental_phone_rental_summary = cls(
            active_count=active_count,
            combined_monthly_cents=combined_monthly_cents,
            per_interval=per_interval,
            upcoming_charges=upcoming_charges,
        )

        return phone_rental_phone_rental_summary
