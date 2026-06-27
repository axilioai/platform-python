from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="WorkflowSaveCodeResponse")


@_attrs_define
class WorkflowSaveCodeResponse:
    """
    Attributes:
        no_op (bool):
        revision (int):
        revision_id (str):
        schema (str | Unset): A URL to the JSON Schema for this object.
    """

    no_op: bool
    revision: int
    revision_id: str
    schema: str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        no_op = self.no_op

        revision = self.revision

        revision_id = self.revision_id

        schema = self.schema

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "no_op": no_op,
                "revision": revision,
                "revision_id": revision_id,
            }
        )
        if schema is not UNSET:
            field_dict["$schema"] = schema

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        no_op = d.pop("no_op")

        revision = d.pop("revision")

        revision_id = d.pop("revision_id")

        schema = d.pop("$schema", UNSET)

        workflow_save_code_response = cls(
            no_op=no_op,
            revision=revision,
            revision_id=revision_id,
            schema=schema,
        )

        return workflow_save_code_response
