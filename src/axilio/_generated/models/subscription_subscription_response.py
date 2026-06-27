from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="SubscriptionSubscriptionResponse")


@_attrs_define
class SubscriptionSubscriptionResponse:
    """
    Attributes:
        balance_display (str):
        balance_microdollars (int):
        billing_cycle (str):
        cancel_at_period_end (bool):
        current_period_end (datetime.datetime):
        current_period_start (datetime.datetime):
        id (str):
        included_balance_display (str):
        included_balance_microdollars (int):
        max_concurrent_runs (int):
        monthly_price (float):
        plan_id (str):
        plan_name (str):
        plan_tier (str):
        price_per_second_microdollars (int):
        status (str):
        yearly_price (float):
        schema (str | Unset): A URL to the JSON Schema for this object.
        canceled_at (datetime.datetime | Unset):
        pending_downgrade_effective_date (datetime.datetime | Unset):
        pending_downgrade_plan_id (str | Unset):
        trial_end (datetime.datetime | Unset):
    """

    balance_display: str
    balance_microdollars: int
    billing_cycle: str
    cancel_at_period_end: bool
    current_period_end: datetime.datetime
    current_period_start: datetime.datetime
    id: str
    included_balance_display: str
    included_balance_microdollars: int
    max_concurrent_runs: int
    monthly_price: float
    plan_id: str
    plan_name: str
    plan_tier: str
    price_per_second_microdollars: int
    status: str
    yearly_price: float
    schema: str | Unset = UNSET
    canceled_at: datetime.datetime | Unset = UNSET
    pending_downgrade_effective_date: datetime.datetime | Unset = UNSET
    pending_downgrade_plan_id: str | Unset = UNSET
    trial_end: datetime.datetime | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        balance_display = self.balance_display

        balance_microdollars = self.balance_microdollars

        billing_cycle = self.billing_cycle

        cancel_at_period_end = self.cancel_at_period_end

        current_period_end = self.current_period_end.isoformat()

        current_period_start = self.current_period_start.isoformat()

        id = self.id

        included_balance_display = self.included_balance_display

        included_balance_microdollars = self.included_balance_microdollars

        max_concurrent_runs = self.max_concurrent_runs

        monthly_price = self.monthly_price

        plan_id = self.plan_id

        plan_name = self.plan_name

        plan_tier = self.plan_tier

        price_per_second_microdollars = self.price_per_second_microdollars

        status = self.status

        yearly_price = self.yearly_price

        schema = self.schema

        canceled_at: str | Unset = UNSET
        if not isinstance(self.canceled_at, Unset):
            canceled_at = self.canceled_at.isoformat()

        pending_downgrade_effective_date: str | Unset = UNSET
        if not isinstance(self.pending_downgrade_effective_date, Unset):
            pending_downgrade_effective_date = self.pending_downgrade_effective_date.isoformat()

        pending_downgrade_plan_id = self.pending_downgrade_plan_id

        trial_end: str | Unset = UNSET
        if not isinstance(self.trial_end, Unset):
            trial_end = self.trial_end.isoformat()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "balance_display": balance_display,
                "balance_microdollars": balance_microdollars,
                "billing_cycle": billing_cycle,
                "cancel_at_period_end": cancel_at_period_end,
                "current_period_end": current_period_end,
                "current_period_start": current_period_start,
                "id": id,
                "included_balance_display": included_balance_display,
                "included_balance_microdollars": included_balance_microdollars,
                "max_concurrent_runs": max_concurrent_runs,
                "monthly_price": monthly_price,
                "plan_id": plan_id,
                "plan_name": plan_name,
                "plan_tier": plan_tier,
                "price_per_second_microdollars": price_per_second_microdollars,
                "status": status,
                "yearly_price": yearly_price,
            }
        )
        if schema is not UNSET:
            field_dict["$schema"] = schema
        if canceled_at is not UNSET:
            field_dict["canceled_at"] = canceled_at
        if pending_downgrade_effective_date is not UNSET:
            field_dict["pending_downgrade_effective_date"] = pending_downgrade_effective_date
        if pending_downgrade_plan_id is not UNSET:
            field_dict["pending_downgrade_plan_id"] = pending_downgrade_plan_id
        if trial_end is not UNSET:
            field_dict["trial_end"] = trial_end

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        balance_display = d.pop("balance_display")

        balance_microdollars = d.pop("balance_microdollars")

        billing_cycle = d.pop("billing_cycle")

        cancel_at_period_end = d.pop("cancel_at_period_end")

        current_period_end = datetime.datetime.fromisoformat(d.pop("current_period_end"))

        current_period_start = datetime.datetime.fromisoformat(d.pop("current_period_start"))

        id = d.pop("id")

        included_balance_display = d.pop("included_balance_display")

        included_balance_microdollars = d.pop("included_balance_microdollars")

        max_concurrent_runs = d.pop("max_concurrent_runs")

        monthly_price = d.pop("monthly_price")

        plan_id = d.pop("plan_id")

        plan_name = d.pop("plan_name")

        plan_tier = d.pop("plan_tier")

        price_per_second_microdollars = d.pop("price_per_second_microdollars")

        status = d.pop("status")

        yearly_price = d.pop("yearly_price")

        schema = d.pop("$schema", UNSET)

        _canceled_at = d.pop("canceled_at", UNSET)
        canceled_at: datetime.datetime | Unset
        if isinstance(_canceled_at, Unset):
            canceled_at = UNSET
        else:
            canceled_at = datetime.datetime.fromisoformat(_canceled_at)

        _pending_downgrade_effective_date = d.pop("pending_downgrade_effective_date", UNSET)
        pending_downgrade_effective_date: datetime.datetime | Unset
        if isinstance(_pending_downgrade_effective_date, Unset):
            pending_downgrade_effective_date = UNSET
        else:
            pending_downgrade_effective_date = datetime.datetime.fromisoformat(_pending_downgrade_effective_date)

        pending_downgrade_plan_id = d.pop("pending_downgrade_plan_id", UNSET)

        _trial_end = d.pop("trial_end", UNSET)
        trial_end: datetime.datetime | Unset
        if isinstance(_trial_end, Unset):
            trial_end = UNSET
        else:
            trial_end = datetime.datetime.fromisoformat(_trial_end)

        subscription_subscription_response = cls(
            balance_display=balance_display,
            balance_microdollars=balance_microdollars,
            billing_cycle=billing_cycle,
            cancel_at_period_end=cancel_at_period_end,
            current_period_end=current_period_end,
            current_period_start=current_period_start,
            id=id,
            included_balance_display=included_balance_display,
            included_balance_microdollars=included_balance_microdollars,
            max_concurrent_runs=max_concurrent_runs,
            monthly_price=monthly_price,
            plan_id=plan_id,
            plan_name=plan_name,
            plan_tier=plan_tier,
            price_per_second_microdollars=price_per_second_microdollars,
            status=status,
            yearly_price=yearly_price,
            schema=schema,
            canceled_at=canceled_at,
            pending_downgrade_effective_date=pending_downgrade_effective_date,
            pending_downgrade_plan_id=pending_downgrade_plan_id,
            trial_end=trial_end,
        )

        return subscription_subscription_response
