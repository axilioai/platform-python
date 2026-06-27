from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.phone_phone_summary import PhonePhoneSummary


T = TypeVar("T", bound="PhonePrivatePhonesResponse")


@_attrs_define
class PhonePrivatePhonesResponse:
    """
    Attributes:
        limit (int):
        offset (int):
        phones (list[PhonePhoneSummary] | None):
        total (int):
        schema (str | Unset): A URL to the JSON Schema for this object.
    """

    limit: int
    offset: int
    phones: list[PhonePhoneSummary] | None
    total: int
    schema: str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        limit = self.limit

        offset = self.offset

        phones: list[dict[str, Any]] | None
        if isinstance(self.phones, list):
            phones = []
            for phones_type_0_item_data in self.phones:
                phones_type_0_item = phones_type_0_item_data.to_dict()
                phones.append(phones_type_0_item)

        else:
            phones = self.phones

        total = self.total

        schema = self.schema

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "limit": limit,
                "offset": offset,
                "phones": phones,
                "total": total,
            }
        )
        if schema is not UNSET:
            field_dict["$schema"] = schema

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.phone_phone_summary import PhonePhoneSummary

        d = dict(src_dict)
        limit = d.pop("limit")

        offset = d.pop("offset")

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

        total = d.pop("total")

        schema = d.pop("$schema", UNSET)

        phone_private_phones_response = cls(
            limit=limit,
            offset=offset,
            phones=phones,
            total=total,
            schema=schema,
        )

        return phone_private_phones_response
