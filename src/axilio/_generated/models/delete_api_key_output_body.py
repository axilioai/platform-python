from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="DeleteAPIKeyOutputBody")


@_attrs_define
class DeleteAPIKeyOutputBody:
    """
    Attributes:
        message (str):
        schema (str | Unset): A URL to the JSON Schema for this object.
    """

    message: str
    schema: str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        message = self.message

        schema = self.schema

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "message": message,
            }
        )
        if schema is not UNSET:
            field_dict["$schema"] = schema

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        message = d.pop("message")

        schema = d.pop("$schema", UNSET)

        delete_api_key_output_body = cls(
            message=message,
            schema=schema,
        )

        return delete_api_key_output_body
