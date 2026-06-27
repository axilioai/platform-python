from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.phone_phone_app_summary import PhonePhoneAppSummary


T = TypeVar("T", bound="PhoneSupportedPhoneAppsResponse")


@_attrs_define
class PhoneSupportedPhoneAppsResponse:
    """
    Attributes:
        phone_apps (list[PhonePhoneAppSummary] | None):
        total (int):
        schema (str | Unset): A URL to the JSON Schema for this object.
    """

    phone_apps: list[PhonePhoneAppSummary] | None
    total: int
    schema: str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        phone_apps: list[dict[str, Any]] | None
        if isinstance(self.phone_apps, list):
            phone_apps = []
            for phone_apps_type_0_item_data in self.phone_apps:
                phone_apps_type_0_item = phone_apps_type_0_item_data.to_dict()
                phone_apps.append(phone_apps_type_0_item)

        else:
            phone_apps = self.phone_apps

        total = self.total

        schema = self.schema

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "phone_apps": phone_apps,
                "total": total,
            }
        )
        if schema is not UNSET:
            field_dict["$schema"] = schema

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.phone_phone_app_summary import PhonePhoneAppSummary

        d = dict(src_dict)

        def _parse_phone_apps(data: object) -> list[PhonePhoneAppSummary] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                phone_apps_type_0 = []
                _phone_apps_type_0 = data
                for phone_apps_type_0_item_data in _phone_apps_type_0:
                    phone_apps_type_0_item = PhonePhoneAppSummary.from_dict(phone_apps_type_0_item_data)

                    phone_apps_type_0.append(phone_apps_type_0_item)

                return phone_apps_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[PhonePhoneAppSummary] | None, data)

        phone_apps = _parse_phone_apps(d.pop("phone_apps"))

        total = d.pop("total")

        schema = d.pop("$schema", UNSET)

        phone_supported_phone_apps_response = cls(
            phone_apps=phone_apps,
            total=total,
            schema=schema,
        )

        return phone_supported_phone_apps_response
