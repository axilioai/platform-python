from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="PhoneRentalRenewPhoneRentalSubscriptionsResponse")


@_attrs_define
class PhoneRentalRenewPhoneRentalSubscriptionsResponse:
    """
    Attributes:
        failed_count (int):
        failed_ids (list[str] | None):
        message (str):
        renewed_count (int):
        renewed_ids (list[str] | None):
        schema (str | Unset): A URL to the JSON Schema for this object.
    """

    failed_count: int
    failed_ids: list[str] | None
    message: str
    renewed_count: int
    renewed_ids: list[str] | None
    schema: str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        failed_count = self.failed_count

        failed_ids: list[str] | None
        if isinstance(self.failed_ids, list):
            failed_ids = self.failed_ids

        else:
            failed_ids = self.failed_ids

        message = self.message

        renewed_count = self.renewed_count

        renewed_ids: list[str] | None
        if isinstance(self.renewed_ids, list):
            renewed_ids = self.renewed_ids

        else:
            renewed_ids = self.renewed_ids

        schema = self.schema

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "failed_count": failed_count,
                "failed_ids": failed_ids,
                "message": message,
                "renewed_count": renewed_count,
                "renewed_ids": renewed_ids,
            }
        )
        if schema is not UNSET:
            field_dict["$schema"] = schema

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        failed_count = d.pop("failed_count")

        def _parse_failed_ids(data: object) -> list[str] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                failed_ids_type_0 = cast(list[str], data)

                return failed_ids_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[str] | None, data)

        failed_ids = _parse_failed_ids(d.pop("failed_ids"))

        message = d.pop("message")

        renewed_count = d.pop("renewed_count")

        def _parse_renewed_ids(data: object) -> list[str] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                renewed_ids_type_0 = cast(list[str], data)

                return renewed_ids_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[str] | None, data)

        renewed_ids = _parse_renewed_ids(d.pop("renewed_ids"))

        schema = d.pop("$schema", UNSET)

        phone_rental_renew_phone_rental_subscriptions_response = cls(
            failed_count=failed_count,
            failed_ids=failed_ids,
            message=message,
            renewed_count=renewed_count,
            renewed_ids=renewed_ids,
            schema=schema,
        )

        return phone_rental_renew_phone_rental_subscriptions_response
