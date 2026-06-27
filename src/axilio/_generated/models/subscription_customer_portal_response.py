from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="SubscriptionCustomerPortalResponse")


@_attrs_define
class SubscriptionCustomerPortalResponse:
    """
    Attributes:
        portal_url (str):
        schema (str | Unset): A URL to the JSON Schema for this object.
    """

    portal_url: str
    schema: str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        portal_url = self.portal_url

        schema = self.schema

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "portal_url": portal_url,
            }
        )
        if schema is not UNSET:
            field_dict["$schema"] = schema

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        portal_url = d.pop("portal_url")

        schema = d.pop("$schema", UNSET)

        subscription_customer_portal_response = cls(
            portal_url=portal_url,
            schema=schema,
        )

        return subscription_customer_portal_response
