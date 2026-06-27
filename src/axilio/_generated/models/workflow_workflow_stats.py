from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="WorkflowWorkflowStats")


@_attrs_define
class WorkflowWorkflowStats:
    """
    Attributes:
        success_rate (float):
        total_runs (int):
    """

    success_rate: float
    total_runs: int

    def to_dict(self) -> dict[str, Any]:
        success_rate = self.success_rate

        total_runs = self.total_runs

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "success_rate": success_rate,
                "total_runs": total_runs,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        success_rate = d.pop("success_rate")

        total_runs = d.pop("total_runs")

        workflow_workflow_stats = cls(
            success_rate=success_rate,
            total_runs=total_runs,
        )

        return workflow_workflow_stats
