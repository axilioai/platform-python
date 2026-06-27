from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="PhoneLocationPhoneCount")


@_attrs_define
class PhoneLocationPhoneCount:
    """
    Attributes:
        available_capacity (int):
        city (str):
        location (str):
        max_capacity (int):
        region (str):
        state (str):
    """

    available_capacity: int
    city: str
    location: str
    max_capacity: int
    region: str
    state: str

    def to_dict(self) -> dict[str, Any]:
        available_capacity = self.available_capacity

        city = self.city

        location = self.location

        max_capacity = self.max_capacity

        region = self.region

        state = self.state

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "available_capacity": available_capacity,
                "city": city,
                "location": location,
                "max_capacity": max_capacity,
                "region": region,
                "state": state,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        available_capacity = d.pop("available_capacity")

        city = d.pop("city")

        location = d.pop("location")

        max_capacity = d.pop("max_capacity")

        region = d.pop("region")

        state = d.pop("state")

        phone_location_phone_count = cls(
            available_capacity=available_capacity,
            city=city,
            location=location,
            max_capacity=max_capacity,
            region=region,
            state=state,
        )

        return phone_location_phone_count
