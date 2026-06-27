from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="UserSettingsUserSettingsResponse")


@_attrs_define
class UserSettingsUserSettingsResponse:
    """
    Attributes:
        schema (str | Unset): A URL to the JSON Schema for this object.
        claude_api_key (str | Unset):
        openai_api_key (str | Unset):
    """

    schema: str | Unset = UNSET
    claude_api_key: str | Unset = UNSET
    openai_api_key: str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        schema = self.schema

        claude_api_key = self.claude_api_key

        openai_api_key = self.openai_api_key

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if schema is not UNSET:
            field_dict["$schema"] = schema
        if claude_api_key is not UNSET:
            field_dict["claude_api_key"] = claude_api_key
        if openai_api_key is not UNSET:
            field_dict["openai_api_key"] = openai_api_key

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        schema = d.pop("$schema", UNSET)

        claude_api_key = d.pop("claude_api_key", UNSET)

        openai_api_key = d.pop("openai_api_key", UNSET)

        user_settings_user_settings_response = cls(
            schema=schema,
            claude_api_key=claude_api_key,
            openai_api_key=openai_api_key,
        )

        return user_settings_user_settings_response
