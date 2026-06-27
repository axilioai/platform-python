"""UsageResource — client.usage.*

All read; available in both local and sandbox modes (scheduled scripts
often want to track their own consumption).
"""

from __future__ import annotations

from datetime import datetime
from typing import Literal

from .._resource import _Resource
from .types import Session, UsageMetrics


class UsageResource(_Resource):
    """client.usage — compute-minute metrics + per-session reports."""

    def metrics(
        self,
        start: datetime,
        end: datetime,
        *,
        granularity: Literal["hourly", "daily", "monthly"] = "daily",
    ) -> UsageMetrics:
        """Aggregated usage in [start, end), bucketed by granularity."""
        raise NotImplementedError("UsageResource.metrics — codegen pending")

    def sessions(
        self,
        start: datetime,
        end: datetime,
        *,
        workflow_id: str | None = None,
    ) -> list[Session]:
        """Individual device sessions in [start, end). Filter by
        workflow when present."""
        raise NotImplementedError("UsageResource.sessions — codegen pending")
