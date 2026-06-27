from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="WorkflowWorkflowCreateResponse")


@_attrs_define
class WorkflowWorkflowCreateResponse:
    """
    Attributes:
        workflow_id (str):
        schema (str | Unset): A URL to the JSON Schema for this object.
    """

    workflow_id: str
    schema: str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        workflow_id = self.workflow_id

        schema = self.schema

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "workflow_id": workflow_id,
            }
        )
        if schema is not UNSET:
            field_dict["$schema"] = schema

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        workflow_id = d.pop("workflow_id")

        schema = d.pop("$schema", UNSET)

        workflow_workflow_create_response = cls(
            workflow_id=workflow_id,
            schema=schema,
        )

        return workflow_workflow_create_response
