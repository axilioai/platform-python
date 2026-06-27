from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="UserSignUpRequest")


@_attrs_define
class UserSignUpRequest:
    """
    Attributes:
        email (str):
        first_name (str):
        last_name (str):
        password (str):
        invite_code (str | Unset):
    """

    email: str
    first_name: str
    last_name: str
    password: str
    invite_code: str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        email = self.email

        first_name = self.first_name

        last_name = self.last_name

        password = self.password

        invite_code = self.invite_code

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "email": email,
                "first_name": first_name,
                "last_name": last_name,
                "password": password,
            }
        )
        if invite_code is not UNSET:
            field_dict["invite_code"] = invite_code

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        email = d.pop("email")

        first_name = d.pop("first_name")

        last_name = d.pop("last_name")

        password = d.pop("password")

        invite_code = d.pop("invite_code", UNSET)

        user_sign_up_request = cls(
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password,
            invite_code=invite_code,
        )

        return user_sign_up_request
