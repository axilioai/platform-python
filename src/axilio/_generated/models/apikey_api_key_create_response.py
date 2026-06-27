from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="ApikeyAPIKeyCreateResponse")


@_attrs_define
class ApikeyAPIKeyCreateResponse:
    """
    Attributes:
        created_at (datetime.datetime):
        id (str):
        key_value (str):
        name (str):
        schema (str | Unset): A URL to the JSON Schema for this object.
    """

    created_at: datetime.datetime
    id: str
    key_value: str
    name: str
    schema: str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        created_at = self.created_at.isoformat()

        id = self.id

        key_value = self.key_value

        name = self.name

        schema = self.schema

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "created_at": created_at,
                "id": id,
                "key_value": key_value,
                "name": name,
            }
        )
        if schema is not UNSET:
            field_dict["$schema"] = schema

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        created_at = datetime.datetime.fromisoformat(d.pop("created_at"))

        id = d.pop("id")

        key_value = d.pop("key_value")

        name = d.pop("name")

        schema = d.pop("$schema", UNSET)

        apikey_api_key_create_response = cls(
            created_at=created_at,
            id=id,
            key_value=key_value,
            name=name,
            schema=schema,
        )

        return apikey_api_key_create_response
