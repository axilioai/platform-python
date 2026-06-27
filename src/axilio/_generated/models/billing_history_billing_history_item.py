from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="BillingHistoryBillingHistoryItem")


@_attrs_define
class BillingHistoryBillingHistoryItem:
    """
    Attributes:
        amount_cents (int):
        amount_dollars (float):
        billing_cycle (str):
        currency (str):
        description (str):
        formatted_amount (str):
        id (str):
        invoice_date (datetime.datetime):
        invoice_number (str):
        plan_name (str):
        status (str):
        due_date (datetime.datetime | Unset):
        hosted_invoice_url (str | Unset):
        invoice_pdf_url (str | Unset):
        paid_at (datetime.datetime | Unset):
    """

    amount_cents: int
    amount_dollars: float
    billing_cycle: str
    currency: str
    description: str
    formatted_amount: str
    id: str
    invoice_date: datetime.datetime
    invoice_number: str
    plan_name: str
    status: str
    due_date: datetime.datetime | Unset = UNSET
    hosted_invoice_url: str | Unset = UNSET
    invoice_pdf_url: str | Unset = UNSET
    paid_at: datetime.datetime | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        amount_cents = self.amount_cents

        amount_dollars = self.amount_dollars

        billing_cycle = self.billing_cycle

        currency = self.currency

        description = self.description

        formatted_amount = self.formatted_amount

        id = self.id

        invoice_date = self.invoice_date.isoformat()

        invoice_number = self.invoice_number

        plan_name = self.plan_name

        status = self.status

        due_date: str | Unset = UNSET
        if not isinstance(self.due_date, Unset):
            due_date = self.due_date.isoformat()

        hosted_invoice_url = self.hosted_invoice_url

        invoice_pdf_url = self.invoice_pdf_url

        paid_at: str | Unset = UNSET
        if not isinstance(self.paid_at, Unset):
            paid_at = self.paid_at.isoformat()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "amount_cents": amount_cents,
                "amount_dollars": amount_dollars,
                "billing_cycle": billing_cycle,
                "currency": currency,
                "description": description,
                "formatted_amount": formatted_amount,
                "id": id,
                "invoice_date": invoice_date,
                "invoice_number": invoice_number,
                "plan_name": plan_name,
                "status": status,
            }
        )
        if due_date is not UNSET:
            field_dict["due_date"] = due_date
        if hosted_invoice_url is not UNSET:
            field_dict["hosted_invoice_url"] = hosted_invoice_url
        if invoice_pdf_url is not UNSET:
            field_dict["invoice_pdf_url"] = invoice_pdf_url
        if paid_at is not UNSET:
            field_dict["paid_at"] = paid_at

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        amount_cents = d.pop("amount_cents")

        amount_dollars = d.pop("amount_dollars")

        billing_cycle = d.pop("billing_cycle")

        currency = d.pop("currency")

        description = d.pop("description")

        formatted_amount = d.pop("formatted_amount")

        id = d.pop("id")

        invoice_date = datetime.datetime.fromisoformat(d.pop("invoice_date"))

        invoice_number = d.pop("invoice_number")

        plan_name = d.pop("plan_name")

        status = d.pop("status")

        _due_date = d.pop("due_date", UNSET)
        due_date: datetime.datetime | Unset
        if isinstance(_due_date, Unset):
            due_date = UNSET
        else:
            due_date = datetime.datetime.fromisoformat(_due_date)

        hosted_invoice_url = d.pop("hosted_invoice_url", UNSET)

        invoice_pdf_url = d.pop("invoice_pdf_url", UNSET)

        _paid_at = d.pop("paid_at", UNSET)
        paid_at: datetime.datetime | Unset
        if isinstance(_paid_at, Unset):
            paid_at = UNSET
        else:
            paid_at = datetime.datetime.fromisoformat(_paid_at)

        billing_history_billing_history_item = cls(
            amount_cents=amount_cents,
            amount_dollars=amount_dollars,
            billing_cycle=billing_cycle,
            currency=currency,
            description=description,
            formatted_amount=formatted_amount,
            id=id,
            invoice_date=invoice_date,
            invoice_number=invoice_number,
            plan_name=plan_name,
            status=status,
            due_date=due_date,
            hosted_invoice_url=hosted_invoice_url,
            invoice_pdf_url=invoice_pdf_url,
            paid_at=paid_at,
        )

        return billing_history_billing_history_item
