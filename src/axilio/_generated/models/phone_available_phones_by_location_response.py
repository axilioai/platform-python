from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.phone_location_phone_count import PhoneLocationPhoneCount


T = TypeVar("T", bound="PhoneAvailablePhonesByLocationResponse")


@_attrs_define
class PhoneAvailablePhonesByLocationResponse:
    """
    Attributes:
        locations (list[PhoneLocationPhoneCount] | None):
        total_locations (int):
        schema (str | Unset): A URL to the JSON Schema for this object.
    """

    locations: list[PhoneLocationPhoneCount] | None
    total_locations: int
    schema: str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        locations: list[dict[str, Any]] | None
        if isinstance(self.locations, list):
            locations = []
            for locations_type_0_item_data in self.locations:
                locations_type_0_item = locations_type_0_item_data.to_dict()
                locations.append(locations_type_0_item)

        else:
            locations = self.locations

        total_locations = self.total_locations

        schema = self.schema

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "locations": locations,
                "total_locations": total_locations,
            }
        )
        if schema is not UNSET:
            field_dict["$schema"] = schema

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.phone_location_phone_count import PhoneLocationPhoneCount

        d = dict(src_dict)

        def _parse_locations(data: object) -> list[PhoneLocationPhoneCount] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                locations_type_0 = []
                _locations_type_0 = data
                for locations_type_0_item_data in _locations_type_0:
                    locations_type_0_item = PhoneLocationPhoneCount.from_dict(locations_type_0_item_data)

                    locations_type_0.append(locations_type_0_item)

                return locations_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[PhoneLocationPhoneCount] | None, data)

        locations = _parse_locations(d.pop("locations"))

        total_locations = d.pop("total_locations")

        schema = d.pop("$schema", UNSET)

        phone_available_phones_by_location_response = cls(
            locations=locations,
            total_locations=total_locations,
            schema=schema,
        )

        return phone_available_phones_by_location_response
