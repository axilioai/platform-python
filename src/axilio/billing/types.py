"""Public dataclasses returned by BillingResource methods.

These are the shapes the design doc specifies for the customer-facing
surface. Wire-level types coming from codegen live under
axilio._generated; this module is hand-curated and is what callers
import.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Literal


@dataclass(frozen=True)
class Balance:
    """Current account balance, in microdollars to avoid float math
    around money. Helpers on this class return human-readable views."""

    microdollars: int
    currency: str = "USD"

    @property
    def dollars(self) -> float:
        return self.microdollars / 1_000_000


@dataclass(frozen=True)
class Subscription:
    """Current subscription plan + period. Plan is one of the closed
    set Axilio recognises (hobby / pro / business / enterprise) plus
    free as the no-subscription default."""

    plan: Literal["free", "hobby", "pro", "business", "enterprise"]
    status: Literal["active", "past_due", "canceled", "trialing"]
    current_period_start: datetime
    current_period_end: datetime
    cancel_at_period_end: bool


@dataclass(frozen=True)
class Invoice:
    """A single historical billing invoice. Mirrors the backend's
    billing_history row, projected for SDK consumers."""

    id: str
    amount_microdollars: int
    currency: str
    status: Literal["paid", "open", "void", "uncollectible"]
    created_at: datetime
    hosted_invoice_url: str | None
