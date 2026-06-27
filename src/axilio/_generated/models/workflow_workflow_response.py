from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.workflow_workflow_stats import WorkflowWorkflowStats
    from ..models.workflow_workflow_summary import WorkflowWorkflowSummary


T = TypeVar("T", bound="WorkflowWorkflowResponse")


@_attrs_define
class WorkflowWorkflowResponse:
    """
    Attributes:
        stats (WorkflowWorkflowStats):
        workflow (WorkflowWorkflowSummary):
        schema (str | Unset): A URL to the JSON Schema for this object.
    """

    stats: WorkflowWorkflowStats
    workflow: WorkflowWorkflowSummary
    schema: str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        stats = self.stats.to_dict()

        workflow = self.workflow.to_dict()

        schema = self.schema

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "stats": stats,
                "workflow": workflow,
            }
        )
        if schema is not UNSET:
            field_dict["$schema"] = schema

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.workflow_workflow_stats import WorkflowWorkflowStats
        from ..models.workflow_workflow_summary import WorkflowWorkflowSummary

        d = dict(src_dict)
        stats = WorkflowWorkflowStats.from_dict(d.pop("stats"))

        workflow = WorkflowWorkflowSummary.from_dict(d.pop("workflow"))

        schema = d.pop("$schema", UNSET)

        workflow_workflow_response = cls(
            stats=stats,
            workflow=workflow,
            schema=schema,
        )

        return workflow_workflow_response
