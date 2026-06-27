"""RunsResource — client.runs.*"""

from __future__ import annotations

from .._resource import _Resource
from .types import Run, RunSummary


class RunsResource(_Resource):
    """client.runs — schedule, query, and cancel workflow executions."""

    def list(
        self,
        *,
        workflow_id: str | None = None,
        limit: int = 50,
    ) -> list[RunSummary]:
        raise NotImplementedError("RunsResource.list — codegen pending")

    def get(self, run_id: str) -> Run:
        raise NotImplementedError("RunsResource.get — codegen pending")

    def create(
        self,
        *,
        workflow_id: str,
        variables: dict[str, str] | None = None,
    ) -> Run:
        """Enqueue a new run of the workflow. Returns immediately
        with status="queued"; poll get() (or subscribe via a future
        SSE endpoint) for terminal status."""
        raise NotImplementedError("RunsResource.create — codegen pending")

    def cancel(self, run_id: str) -> Run:
        """Request cancellation. The backend transitions to "canceled"
        once the run actually stops — which can be near-instant if
        queued, or take a moment if currently executing inside a
        sandbox."""
        raise NotImplementedError("RunsResource.cancel — codegen pending")
