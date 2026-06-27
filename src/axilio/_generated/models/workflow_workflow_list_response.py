from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.workflow_workflow_response import WorkflowWorkflowResponse


T = TypeVar("T", bound="WorkflowWorkflowListResponse")


@_attrs_define
class WorkflowWorkflowListResponse:
    """
    Attributes:
        limit (int):
        offset (int):
        total (int):
        workflows (list[WorkflowWorkflowResponse] | None):
        schema (str | Unset): A URL to the JSON Schema for this object.
    """

    limit: int
    offset: int
    total: int
    workflows: list[WorkflowWorkflowResponse] | None
    schema: str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        limit = self.limit

        offset = self.offset

        total = self.total

        workflows: list[dict[str, Any]] | None
        if isinstance(self.workflows, list):
            workflows = []
            for workflows_type_0_item_data in self.workflows:
                workflows_type_0_item = workflows_type_0_item_data.to_dict()
                workflows.append(workflows_type_0_item)

        else:
            workflows = self.workflows

        schema = self.schema

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "limit": limit,
                "offset": offset,
                "total": total,
                "workflows": workflows,
            }
        )
        if schema is not UNSET:
            field_dict["$schema"] = schema

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.workflow_workflow_response import WorkflowWorkflowResponse

        d = dict(src_dict)
        limit = d.pop("limit")

        offset = d.pop("offset")

        total = d.pop("total")

        def _parse_workflows(data: object) -> list[WorkflowWorkflowResponse] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                workflows_type_0 = []
                _workflows_type_0 = data
                for workflows_type_0_item_data in _workflows_type_0:
                    workflows_type_0_item = WorkflowWorkflowResponse.from_dict(workflows_type_0_item_data)

                    workflows_type_0.append(workflows_type_0_item)

                return workflows_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[WorkflowWorkflowResponse] | None, data)

        workflows = _parse_workflows(d.pop("workflows"))

        schema = d.pop("$schema", UNSET)

        workflow_workflow_list_response = cls(
            limit=limit,
            offset=offset,
            total=total,
            workflows=workflows,
            schema=schema,
        )

        return workflow_workflow_list_response
