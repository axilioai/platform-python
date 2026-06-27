from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="PhoneRentalCancelPhoneRentalSubscriptionsRequest")


@_attrs_define
class PhoneRentalCancelPhoneRentalSubscriptionsRequest:
    """
    Attributes:
        subscription_ids (list[str] | None):
        schema (str | Unset): A URL to the JSON Schema for this object.
    """

    subscription_ids: list[str] | None
    schema: str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        subscription_ids: list[str] | None
        if isinstance(self.subscription_ids, list):
            subscription_ids = self.subscription_ids

        else:
            subscription_ids = self.subscription_ids

        schema = self.schema

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "subscription_ids": subscription_ids,
            }
        )
        if schema is not UNSET:
            field_dict["$schema"] = schema

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_subscription_ids(data: object) -> list[str] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                subscription_ids_type_0 = cast(list[str], data)

                return subscription_ids_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[str] | None, data)

        subscription_ids = _parse_subscription_ids(d.pop("subscription_ids"))

        schema = d.pop("$schema", UNSET)

        phone_rental_cancel_phone_rental_subscriptions_request = cls(
            subscription_ids=subscription_ids,
            schema=schema,
        )

        return phone_rental_cancel_phone_rental_subscriptions_request
