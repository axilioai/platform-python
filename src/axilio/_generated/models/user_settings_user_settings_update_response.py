from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="UserSettingsUserSettingsUpdateResponse")


@_attrs_define
class UserSettingsUserSettingsUpdateResponse:
    """
    Attributes:
        message (str):
        success (bool):
        schema (str | Unset): A URL to the JSON Schema for this object.
    """

    message: str
    success: bool
    schema: str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        message = self.message

        success = self.success

        schema = self.schema

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "message": message,
                "success": success,
            }
        )
        if schema is not UNSET:
            field_dict["$schema"] = schema

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        message = d.pop("message")

        success = d.pop("success")

        schema = d.pop("$schema", UNSET)

        user_settings_user_settings_update_response = cls(
            message=message,
            success=success,
            schema=schema,
        )

        return user_settings_user_settings_update_response
