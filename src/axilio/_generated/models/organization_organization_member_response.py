from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="OrganizationOrganizationMemberResponse")


@_attrs_define
class OrganizationOrganizationMemberResponse:
    """
    Attributes:
        id (str):
        organization_id (str):
        role (str):
        user_id (str):
        schema (str | Unset): A URL to the JSON Schema for this object.
        created_at (datetime.datetime | Unset):
        email (str | Unset):
        name (str | Unset):
    """

    id: str
    organization_id: str
    role: str
    user_id: str
    schema: str | Unset = UNSET
    created_at: datetime.datetime | Unset = UNSET
    email: str | Unset = UNSET
    name: str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        organization_id = self.organization_id

        role = self.role

        user_id = self.user_id

        schema = self.schema

        created_at: str | Unset = UNSET
        if not isinstance(self.created_at, Unset):
            created_at = self.created_at.isoformat()

        email = self.email

        name = self.name

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "id": id,
                "organization_id": organization_id,
                "role": role,
                "user_id": user_id,
            }
        )
        if schema is not UNSET:
            field_dict["$schema"] = schema
        if created_at is not UNSET:
            field_dict["created_at"] = created_at
        if email is not UNSET:
            field_dict["email"] = email
        if name is not UNSET:
            field_dict["name"] = name

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        organization_id = d.pop("organization_id")

        role = d.pop("role")

        user_id = d.pop("user_id")

        schema = d.pop("$schema", UNSET)

        _created_at = d.pop("created_at", UNSET)
        created_at: datetime.datetime | Unset
        if isinstance(_created_at, Unset):
            created_at = UNSET
        else:
            created_at = datetime.datetime.fromisoformat(_created_at)

        email = d.pop("email", UNSET)

        name = d.pop("name", UNSET)

        organization_organization_member_response = cls(
            id=id,
            organization_id=organization_id,
            role=role,
            user_id=user_id,
            schema=schema,
            created_at=created_at,
            email=email,
            name=name,
        )

        return organization_organization_member_response
