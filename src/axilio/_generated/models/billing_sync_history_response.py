from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="BillingSyncHistoryResponse")


@_attrs_define
class BillingSyncHistoryResponse:
    """
    Attributes:
        message (str):
        synced_count (int):
        schema (str | Unset): A URL to the JSON Schema for this object.
    """

    message: str
    synced_count: int
    schema: str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        message = self.message

        synced_count = self.synced_count

        schema = self.schema

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "message": message,
                "synced_count": synced_count,
            }
        )
        if schema is not UNSET:
            field_dict["$schema"] = schema

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        message = d.pop("message")

        synced_count = d.pop("synced_count")

        schema = d.pop("$schema", UNSET)

        billing_sync_history_response = cls(
            message=message,
            synced_count=synced_count,
            schema=schema,
        )

        return billing_sync_history_response
