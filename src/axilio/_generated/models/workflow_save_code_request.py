from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="WorkflowSaveCodeRequest")


@_attrs_define
class WorkflowSaveCodeRequest:
    """
    Attributes:
        source (str):
        schema (str | Unset): A URL to the JSON Schema for this object.
        message (str | Unset):
    """

    source: str
    schema: str | Unset = UNSET
    message: str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        source = self.source

        schema = self.schema

        message = self.message

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "source": source,
            }
        )
        if schema is not UNSET:
            field_dict["$schema"] = schema
        if message is not UNSET:
            field_dict["message"] = message

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        source = d.pop("source")

        schema = d.pop("$schema", UNSET)

        message = d.pop("message", UNSET)

        workflow_save_code_request = cls(
            source=source,
            schema=schema,
            message=message,
        )

        return workflow_save_code_request
