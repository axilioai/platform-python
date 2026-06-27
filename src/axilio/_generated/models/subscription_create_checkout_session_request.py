from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="SubscriptionCreateCheckoutSessionRequest")


@_attrs_define
class SubscriptionCreateCheckoutSessionRequest:
    """
    Attributes:
        billing_cycle (str):
        plan_id (str):
        schema (str | Unset): A URL to the JSON Schema for this object.
    """

    billing_cycle: str
    plan_id: str
    schema: str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        billing_cycle = self.billing_cycle

        plan_id = self.plan_id

        schema = self.schema

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "billing_cycle": billing_cycle,
                "plan_id": plan_id,
            }
        )
        if schema is not UNSET:
            field_dict["$schema"] = schema

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        billing_cycle = d.pop("billing_cycle")

        plan_id = d.pop("plan_id")

        schema = d.pop("$schema", UNSET)

        subscription_create_checkout_session_request = cls(
            billing_cycle=billing_cycle,
            plan_id=plan_id,
            schema=schema,
        )

        return subscription_create_checkout_session_request
