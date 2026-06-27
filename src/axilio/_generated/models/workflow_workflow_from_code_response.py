from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="WorkflowWorkflowFromCodeResponse")


@_attrs_define
class WorkflowWorkflowFromCodeResponse:
    """
    Attributes:
        revision (int):
        revision_id (str):
        workflow_id (str):
        schema (str | Unset): A URL to the JSON Schema for this object.
    """

    revision: int
    revision_id: str
    workflow_id: str
    schema: str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        revision = self.revision

        revision_id = self.revision_id

        workflow_id = self.workflow_id

        schema = self.schema

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "revision": revision,
                "revision_id": revision_id,
                "workflow_id": workflow_id,
            }
        )
        if schema is not UNSET:
            field_dict["$schema"] = schema

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        revision = d.pop("revision")

        revision_id = d.pop("revision_id")

        workflow_id = d.pop("workflow_id")

        schema = d.pop("$schema", UNSET)

        workflow_workflow_from_code_response = cls(
            revision=revision,
            revision_id=revision_id,
            workflow_id=workflow_id,
            schema=schema,
        )

        return workflow_workflow_from_code_response
