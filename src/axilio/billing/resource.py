"""BillingResource — client.billing.*

Read methods (balance, subscription, invoices) work in both local and
sandbox mode. Upgrade and downgrade are local-only — scheduled scripts
can't change their owner's subscription out from under them.

Method bodies are stubs until codegen + manual wiring lands; signatures
match the design doc so the public surface is stable from day one.
"""

from __future__ import annotations

from datetime import datetime

from .._resource import _Resource
from .types import Balance, Invoice, Subscription


class BillingResource(_Resource):
    """client.billing — balance, subscription, invoices."""

    def balance(self) -> Balance:
        """Current account balance. Read-only; works in both modes."""
        raise NotImplementedError("BillingResource.balance — codegen pending")

    def subscription(self) -> Subscription:
        """Active subscription (plan, period, cancellation state)."""
        raise NotImplementedError("BillingResource.subscription — codegen pending")

    def invoices(self, start: datetime, end: datetime) -> list[Invoice]:
        """Historical invoices in [start, end). Half-open interval
        matches the backend's billing_history query."""
        raise NotImplementedError("BillingResource.invoices — codegen pending")

    def upgrade(self, *, plan: str) -> Subscription:
        """Move to a higher-tier plan. Local-mode only."""
        self._require_local_mode("billing.upgrade")
        raise NotImplementedError("BillingResource.upgrade — codegen pending")

    def downgrade(self, *, plan: str) -> Subscription:
        """Move to a lower-tier plan. Local-mode only. The actual plan
        change applies at the end of the current billing period — the
        backend marks cancel_at_period_end on the subscription."""
        self._require_local_mode("billing.downgrade")
        raise NotImplementedError("BillingResource.downgrade — codegen pending")
