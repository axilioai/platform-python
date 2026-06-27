from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="UserInviteCodeValidationResponse")


@_attrs_define
class UserInviteCodeValidationResponse:
    """
    Attributes:
        valid (bool):
        message (str | Unset):
    """

    valid: bool
    message: str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        valid = self.valid

        message = self.message

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "valid": valid,
            }
        )
        if message is not UNSET:
            field_dict["message"] = message

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        valid = d.pop("valid")

        message = d.pop("message", UNSET)

        user_invite_code_validation_response = cls(
            valid=valid,
            message=message,
        )

        return user_invite_code_validation_response
