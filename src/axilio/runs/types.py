"""Public types for run scheduling + reporting."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Literal

RunStatus = Literal[
    "queued",
    "starting",
    "running",
    "succeeded",
    "failed",
    "canceled",
]


@dataclass(frozen=True)
class RunSummary:
    """Compact run row, as returned by list(). Drops large fields
    (variables, logs) — fetch via get() when needed."""

    id: str
    workflow_id: str
    status: RunStatus
    created_at: datetime
    started_at: datetime | None
    finished_at: datetime | None


@dataclass(frozen=True)
class Run:
    """Full run record. Includes the variables passed at creation time
    plus the workflow's resolved code at the moment of dispatch (so
    later edits to the workflow don't change historical runs)."""

    id: str
    workflow_id: str
    status: RunStatus
    variables: dict[str, str]
    code: str
    created_at: datetime
    started_at: datetime | None
    finished_at: datetime | None
    error: str | None
