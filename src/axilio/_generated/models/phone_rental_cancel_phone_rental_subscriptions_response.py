from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="PhoneRentalCancelPhoneRentalSubscriptionsResponse")


@_attrs_define
class PhoneRentalCancelPhoneRentalSubscriptionsResponse:
    """
    Attributes:
        canceled_count (int):
        canceled_ids (list[str] | None):
        failed_count (int):
        failed_ids (list[str] | None):
        message (str):
        schema (str | Unset): A URL to the JSON Schema for this object.
    """

    canceled_count: int
    canceled_ids: list[str] | None
    failed_count: int
    failed_ids: list[str] | None
    message: str
    schema: str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        canceled_count = self.canceled_count

        canceled_ids: list[str] | None
        if isinstance(self.canceled_ids, list):
            canceled_ids = self.canceled_ids

        else:
            canceled_ids = self.canceled_ids

        failed_count = self.failed_count

        failed_ids: list[str] | None
        if isinstance(self.failed_ids, list):
            failed_ids = self.failed_ids

        else:
            failed_ids = self.failed_ids

        message = self.message

        schema = self.schema

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "canceled_count": canceled_count,
                "canceled_ids": canceled_ids,
                "failed_count": failed_count,
                "failed_ids": failed_ids,
                "message": message,
            }
        )
        if schema is not UNSET:
            field_dict["$schema"] = schema

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        canceled_count = d.pop("canceled_count")

        def _parse_canceled_ids(data: object) -> list[str] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                canceled_ids_type_0 = cast(list[str], data)

                return canceled_ids_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[str] | None, data)

        canceled_ids = _parse_canceled_ids(d.pop("canceled_ids"))

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

        schema = d.pop("$schema", UNSET)

        phone_rental_cancel_phone_rental_subscriptions_response = cls(
            canceled_count=canceled_count,
            canceled_ids=canceled_ids,
            failed_count=failed_count,
            failed_ids=failed_ids,
            message=message,
            schema=schema,
        )

        return phone_rental_cancel_phone_rental_subscriptions_response
