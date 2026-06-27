from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.phone_phone_summary import PhonePhoneSummary


T = TypeVar("T", bound="PhoneAvailablePhonesResponse")


@_attrs_define
class PhoneAvailablePhonesResponse:
    """
    Attributes:
        android_count (int):
        iphone_count (int):
        phones (list[PhonePhoneSummary] | None):
        schema (str | Unset): A URL to the JSON Schema for this object.
    """

    android_count: int
    iphone_count: int
    phones: list[PhonePhoneSummary] | None
    schema: str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        android_count = self.android_count

        iphone_count = self.iphone_count

        phones: list[dict[str, Any]] | None
        if isinstance(self.phones, list):
            phones = []
            for phones_type_0_item_data in self.phones:
                phones_type_0_item = phones_type_0_item_data.to_dict()
                phones.append(phones_type_0_item)

        else:
            phones = self.phones

        schema = self.schema

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "android_count": android_count,
                "iphone_count": iphone_count,
                "phones": phones,
            }
        )
        if schema is not UNSET:
            field_dict["$schema"] = schema

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.phone_phone_summary import PhonePhoneSummary

        d = dict(src_dict)
        android_count = d.pop("android_count")

        iphone_count = d.pop("iphone_count")

        def _parse_phones(data: object) -> list[PhonePhoneSummary] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                phones_type_0 = []
                _phones_type_0 = data
                for phones_type_0_item_data in _phones_type_0:
                    phones_type_0_item = PhonePhoneSummary.from_dict(phones_type_0_item_data)

                    phones_type_0.append(phones_type_0_item)

                return phones_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[PhonePhoneSummary] | None, data)

        phones = _parse_phones(d.pop("phones"))

        schema = d.pop("$schema", UNSET)

        phone_available_phones_response = cls(
            android_count=android_count,
            iphone_count=iphone_count,
            phones=phones,
            schema=schema,
        )

        return phone_available_phones_response
