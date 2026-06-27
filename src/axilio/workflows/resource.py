"""WorkflowsResource — client.workflows.*"""

from __future__ import annotations

from .._resource import _Resource
from .types import Workflow, WorkflowSummary


class WorkflowsResource(_Resource):
    """client.workflows — CRUD for the scripts users author in the
    dashboard and the SDK schedules."""

    def list(self) -> list[WorkflowSummary]:
        raise NotImplementedError("WorkflowsResource.list — codegen pending")

    def get(self, workflow_id: str) -> Workflow:
        raise NotImplementedError("WorkflowsResource.get — codegen pending")

    def create(
        self,
        *,
        name: str,
        code: str,
        description: str | None = None,
    ) -> Workflow:
        raise NotImplementedError("WorkflowsResource.create — codegen pending")

    def update(
        self,
        workflow_id: str,
        *,
        name: str | None = None,
        code: str | None = None,
        description: str | None = None,
    ) -> Workflow:
        raise NotImplementedError("WorkflowsResource.update — codegen pending")

    def delete(self, workflow_id: str) -> None:
        raise NotImplementedError("WorkflowsResource.delete — codegen pending")
