from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="OrganizationCreateInvitationRequest")


@_attrs_define
class OrganizationCreateInvitationRequest:
    """
    Attributes:
        email (str):
        role (str):
        schema (str | Unset): A URL to the JSON Schema for this object.
        redirect_url (str | Unset):
    """

    email: str
    role: str
    schema: str | Unset = UNSET
    redirect_url: str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        email = self.email

        role = self.role

        schema = self.schema

        redirect_url = self.redirect_url

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "email": email,
                "role": role,
            }
        )
        if schema is not UNSET:
            field_dict["$schema"] = schema
        if redirect_url is not UNSET:
            field_dict["redirect_url"] = redirect_url

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        email = d.pop("email")

        role = d.pop("role")

        schema = d.pop("$schema", UNSET)

        redirect_url = d.pop("redirect_url", UNSET)

        organization_create_invitation_request = cls(
            email=email,
            role=role,
            schema=schema,
            redirect_url=redirect_url,
        )

        return organization_create_invitation_request
