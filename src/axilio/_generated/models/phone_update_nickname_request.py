from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="PhoneUpdateNicknameRequest")


@_attrs_define
class PhoneUpdateNicknameRequest:
    """
    Attributes:
        nickname (str):
        schema (str | Unset): A URL to the JSON Schema for this object.
    """

    nickname: str
    schema: str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        nickname = self.nickname

        schema = self.schema

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "nickname": nickname,
            }
        )
        if schema is not UNSET:
            field_dict["$schema"] = schema

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        nickname = d.pop("nickname")

        schema = d.pop("$schema", UNSET)

        phone_update_nickname_request = cls(
            nickname=nickname,
            schema=schema,
        )

        return phone_update_nickname_request
