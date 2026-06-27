from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="OrganizationInvitationResponse")


@_attrs_define
class OrganizationInvitationResponse:
    """
    Attributes:
        email (str):
        id (str):
        invited_by (str):
        organization_id (str):
        role (str):
        schema (str | Unset): A URL to the JSON Schema for this object.
        created_at (datetime.datetime | Unset):
        external_invitation_id (str | Unset):
        invited_by_name (str | Unset):
    """

    email: str
    id: str
    invited_by: str
    organization_id: str
    role: str
    schema: str | Unset = UNSET
    created_at: datetime.datetime | Unset = UNSET
    external_invitation_id: str | Unset = UNSET
    invited_by_name: str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        email = self.email

        id = self.id

        invited_by = self.invited_by

        organization_id = self.organization_id

        role = self.role

        schema = self.schema

        created_at: str | Unset = UNSET
        if not isinstance(self.created_at, Unset):
            created_at = self.created_at.isoformat()

        external_invitation_id = self.external_invitation_id

        invited_by_name = self.invited_by_name

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "email": email,
                "id": id,
                "invited_by": invited_by,
                "organization_id": organization_id,
                "role": role,
            }
        )
        if schema is not UNSET:
            field_dict["$schema"] = schema
        if created_at is not UNSET:
            field_dict["created_at"] = created_at
        if external_invitation_id is not UNSET:
            field_dict["external_invitation_id"] = external_invitation_id
        if invited_by_name is not UNSET:
            field_dict["invited_by_name"] = invited_by_name

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        email = d.pop("email")

        id = d.pop("id")

        invited_by = d.pop("invited_by")

        organization_id = d.pop("organization_id")

        role = d.pop("role")

        schema = d.pop("$schema", UNSET)

        _created_at = d.pop("created_at", UNSET)
        created_at: datetime.datetime | Unset
        if isinstance(_created_at, Unset):
            created_at = UNSET
        else:
            created_at = datetime.datetime.fromisoformat(_created_at)

        external_invitation_id = d.pop("external_invitation_id", UNSET)

        invited_by_name = d.pop("invited_by_name", UNSET)

        organization_invitation_response = cls(
            email=email,
            id=id,
            invited_by=invited_by,
            organization_id=organization_id,
            role=role,
            schema=schema,
            created_at=created_at,
            external_invitation_id=external_invitation_id,
            invited_by_name=invited_by_name,
        )

        return organization_invitation_response
