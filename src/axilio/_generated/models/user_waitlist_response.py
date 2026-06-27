from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="UserWaitlistResponse")


@_attrs_define
class UserWaitlistResponse:
    """
    Attributes:
        message (str):
        success (bool):
    """

    message: str
    success: bool

    def to_dict(self) -> dict[str, Any]:
        message = self.message

        success = self.success

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "message": message,
                "success": success,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        message = d.pop("message")

        success = d.pop("success")

        user_waitlist_response = cls(
            message=message,
            success=success,
        )

        return user_waitlist_response
