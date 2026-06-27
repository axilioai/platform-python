"""Public types for usage queries."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Literal


@dataclass(frozen=True)
class UsageBucket:
    """A single time-bucketed slice of compute-minute usage."""

    bucket_start: datetime
    minutes: float
    cost_microdollars: int


@dataclass(frozen=True)
class UsageMetrics:
    """Aggregated usage across a [start, end) window. `buckets` is
    keyed by the requested granularity (daily / hourly); `total_*`
    are the rollups across the whole window."""

    start: datetime
    end: datetime
    granularity: Literal["hourly", "daily", "monthly"]
    buckets: list[UsageBucket]
    total_minutes: float
    total_cost_microdollars: int


@dataclass(frozen=True)
class Session:
    """A single device session as billed. Mirrors one device_allocation
    row from the backend's perspective."""

    id: str
    workflow_id: str | None
    run_id: str | None
    device_id: str
    started_at: datetime
    ended_at: datetime | None
    minutes: float
    cost_microdollars: int
