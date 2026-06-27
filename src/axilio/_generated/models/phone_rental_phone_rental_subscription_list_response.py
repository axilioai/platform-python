from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.phone_rental_phone_rental_subscription_response import PhoneRentalPhoneRentalSubscriptionResponse
    from ..models.phone_rental_phone_rental_summary import PhoneRentalPhoneRentalSummary


T = TypeVar("T", bound="PhoneRentalPhoneRentalSubscriptionListResponse")


@_attrs_define
class PhoneRentalPhoneRentalSubscriptionListResponse:
    """
    Attributes:
        has_more (bool):
        subscriptions (list[PhoneRentalPhoneRentalSubscriptionResponse] | None):
        summary (PhoneRentalPhoneRentalSummary):
        total (int):
        schema (str | Unset): A URL to the JSON Schema for this object.
    """

    has_more: bool
    subscriptions: list[PhoneRentalPhoneRentalSubscriptionResponse] | None
    summary: PhoneRentalPhoneRentalSummary
    total: int
    schema: str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        has_more = self.has_more

        subscriptions: list[dict[str, Any]] | None
        if isinstance(self.subscriptions, list):
            subscriptions = []
            for subscriptions_type_0_item_data in self.subscriptions:
                subscriptions_type_0_item = subscriptions_type_0_item_data.to_dict()
                subscriptions.append(subscriptions_type_0_item)

        else:
            subscriptions = self.subscriptions

        summary = self.summary.to_dict()

        total = self.total

        schema = self.schema

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "has_more": has_more,
                "subscriptions": subscriptions,
                "summary": summary,
                "total": total,
            }
        )
        if schema is not UNSET:
            field_dict["$schema"] = schema

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.phone_rental_phone_rental_subscription_response import PhoneRentalPhoneRentalSubscriptionResponse
        from ..models.phone_rental_phone_rental_summary import PhoneRentalPhoneRentalSummary

        d = dict(src_dict)
        has_more = d.pop("has_more")

        def _parse_subscriptions(data: object) -> list[PhoneRentalPhoneRentalSubscriptionResponse] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                subscriptions_type_0 = []
                _subscriptions_type_0 = data
                for subscriptions_type_0_item_data in _subscriptions_type_0:
                    subscriptions_type_0_item = PhoneRentalPhoneRentalSubscriptionResponse.from_dict(
                        subscriptions_type_0_item_data
                    )

                    subscriptions_type_0.append(subscriptions_type_0_item)

                return subscriptions_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[PhoneRentalPhoneRentalSubscriptionResponse] | None, data)

        subscriptions = _parse_subscriptions(d.pop("subscriptions"))

        summary = PhoneRentalPhoneRentalSummary.from_dict(d.pop("summary"))

        total = d.pop("total")

        schema = d.pop("$schema", UNSET)

        phone_rental_phone_rental_subscription_list_response = cls(
            has_more=has_more,
            subscriptions=subscriptions,
            summary=summary,
            total=total,
            schema=schema,
        )

        return phone_rental_phone_rental_subscription_list_response
