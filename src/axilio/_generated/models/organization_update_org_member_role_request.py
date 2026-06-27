from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="OrganizationUpdateOrgMemberRoleRequest")


@_attrs_define
class OrganizationUpdateOrgMemberRoleRequest:
    """
    Attributes:
        role (str):
        schema (str | Unset): A URL to the JSON Schema for this object.
    """

    role: str
    schema: str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        role = self.role

        schema = self.schema

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "role": role,
            }
        )
        if schema is not UNSET:
            field_dict["$schema"] = schema

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        role = d.pop("role")

        schema = d.pop("$schema", UNSET)

        organization_update_org_member_role_request = cls(
            role=role,
            schema=schema,
        )

        return organization_update_org_member_role_request
