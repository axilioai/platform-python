from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="UserUserResponse")


@_attrs_define
class UserUserResponse:
    """
    Attributes:
        created_at (str):
        email (str):
        id (str):
        is_admin (bool):
        is_verified (bool):
        updated_at (str):
        schema (str | Unset): A URL to the JSON Schema for this object.
    """

    created_at: str
    email: str
    id: str
    is_admin: bool
    is_verified: bool
    updated_at: str
    schema: str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        created_at = self.created_at

        email = self.email

        id = self.id

        is_admin = self.is_admin

        is_verified = self.is_verified

        updated_at = self.updated_at

        schema = self.schema

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "created_at": created_at,
                "email": email,
                "id": id,
                "is_admin": is_admin,
                "is_verified": is_verified,
                "updated_at": updated_at,
            }
        )
        if schema is not UNSET:
            field_dict["$schema"] = schema

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        created_at = d.pop("created_at")

        email = d.pop("email")

        id = d.pop("id")

        is_admin = d.pop("is_admin")

        is_verified = d.pop("is_verified")

        updated_at = d.pop("updated_at")

        schema = d.pop("$schema", UNSET)

        user_user_response = cls(
            created_at=created_at,
            email=email,
            id=id,
            is_admin=is_admin,
            is_verified=is_verified,
            updated_at=updated_at,
            schema=schema,
        )

        return user_user_response
