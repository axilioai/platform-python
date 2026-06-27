"""Public types for workflow CRUD."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class WorkflowSummary:
    """Compact workflow row as returned by list(). Drop the `code`
    body to keep list responses light — fetch via get() when needed."""

    id: str
    name: str
    description: str | None
    created_at: datetime
    updated_at: datetime
    last_run_at: datetime | None


@dataclass(frozen=True)
class Workflow:
    """Full workflow including the script body. Returned by get(),
    create(), update()."""

    id: str
    name: str
    description: str | None
    code: str
    created_at: datetime
    updated_at: datetime
    last_run_at: datetime | None
