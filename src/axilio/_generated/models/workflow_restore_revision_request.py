from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="WorkflowRestoreRevisionRequest")


@_attrs_define
class WorkflowRestoreRevisionRequest:
    """
    Attributes:
        revision_id (str):
        schema (str | Unset): A URL to the JSON Schema for this object.
    """

    revision_id: str
    schema: str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        revision_id = self.revision_id

        schema = self.schema

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "revision_id": revision_id,
            }
        )
        if schema is not UNSET:
            field_dict["$schema"] = schema

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        revision_id = d.pop("revision_id")

        schema = d.pop("$schema", UNSET)

        workflow_restore_revision_request = cls(
            revision_id=revision_id,
            schema=schema,
        )

        return workflow_restore_revision_request
