from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="SubscriptionCancelSubscriptionResponse")


@_attrs_define
class SubscriptionCancelSubscriptionResponse:
    """
    Attributes:
        cancel_at (datetime.datetime):
        message (str):
        schema (str | Unset): A URL to the JSON Schema for this object.
    """

    cancel_at: datetime.datetime
    message: str
    schema: str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        cancel_at = self.cancel_at.isoformat()

        message = self.message

        schema = self.schema

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "cancel_at": cancel_at,
                "message": message,
            }
        )
        if schema is not UNSET:
            field_dict["$schema"] = schema

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        cancel_at = datetime.datetime.fromisoformat(d.pop("cancel_at"))

        message = d.pop("message")

        schema = d.pop("$schema", UNSET)

        subscription_cancel_subscription_response = cls(
            cancel_at=cancel_at,
            message=message,
            schema=schema,
        )

        return subscription_cancel_subscription_response
