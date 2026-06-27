from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="UserProvisionResponse")


@_attrs_define
class UserProvisionResponse:
    """
    Attributes:
        user_id (str):
        org_slug (str | Unset):
    """

    user_id: str
    org_slug: str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        user_id = self.user_id

        org_slug = self.org_slug

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "user_id": user_id,
            }
        )
        if org_slug is not UNSET:
            field_dict["org_slug"] = org_slug

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        user_id = d.pop("user_id")

        org_slug = d.pop("org_slug", UNSET)

        user_provision_response = cls(
            user_id=user_id,
            org_slug=org_slug,
        )

        return user_provision_response
