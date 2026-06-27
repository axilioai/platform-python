from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="OrganizationAddOrgMemberRequest")


@_attrs_define
class OrganizationAddOrgMemberRequest:
    """
    Attributes:
        role (str):
        user_id (str):
        schema (str | Unset): A URL to the JSON Schema for this object.
    """

    role: str
    user_id: str
    schema: str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        role = self.role

        user_id = self.user_id

        schema = self.schema

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "role": role,
                "user_id": user_id,
            }
        )
        if schema is not UNSET:
            field_dict["$schema"] = schema

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        role = d.pop("role")

        user_id = d.pop("user_id")

        schema = d.pop("$schema", UNSET)

        organization_add_org_member_request = cls(
            role=role,
            user_id=user_id,
            schema=schema,
        )

        return organization_add_org_member_request
