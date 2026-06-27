from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="SubscriptionDowngradeRequest")


@_attrs_define
class SubscriptionDowngradeRequest:
    """
    Attributes:
        plan_id (str):
        schema (str | Unset): A URL to the JSON Schema for this object.
        reason (str | Unset):
    """

    plan_id: str
    schema: str | Unset = UNSET
    reason: str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        plan_id = self.plan_id

        schema = self.schema

        reason = self.reason

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "plan_id": plan_id,
            }
        )
        if schema is not UNSET:
            field_dict["$schema"] = schema
        if reason is not UNSET:
            field_dict["reason"] = reason

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        plan_id = d.pop("plan_id")

        schema = d.pop("$schema", UNSET)

        reason = d.pop("reason", UNSET)

        subscription_downgrade_request = cls(
            plan_id=plan_id,
            schema=schema,
            reason=reason,
        )

        return subscription_downgrade_request
