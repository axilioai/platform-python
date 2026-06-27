from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="PhoneRentalPhoneRentalSubscriptionResponse")


@_attrs_define
class PhoneRentalPhoneRentalSubscriptionResponse:
    """
    Attributes:
        cancel_at_period_end (bool):
        current_period_end (datetime.datetime):
        current_period_start (datetime.datetime):
        id (str):
        organization_id (str):
        payment_status (str):
        plan_id (str):
        plan_interval (str):
        plan_name (str):
        plan_price_cents (int):
        status (str):
        canceled_at (datetime.datetime | Unset):
        phone_id (str | Unset):
        phone_name (str | Unset):
        phone_nickname (str | Unset):
    """

    cancel_at_period_end: bool
    current_period_end: datetime.datetime
    current_period_start: datetime.datetime
    id: str
    organization_id: str
    payment_status: str
    plan_id: str
    plan_interval: str
    plan_name: str
    plan_price_cents: int
    status: str
    canceled_at: datetime.datetime | Unset = UNSET
    phone_id: str | Unset = UNSET
    phone_name: str | Unset = UNSET
    phone_nickname: str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        cancel_at_period_end = self.cancel_at_period_end

        current_period_end = self.current_period_end.isoformat()

        current_period_start = self.current_period_start.isoformat()

        id = self.id

        organization_id = self.organization_id

        payment_status = self.payment_status

        plan_id = self.plan_id

        plan_interval = self.plan_interval

        plan_name = self.plan_name

        plan_price_cents = self.plan_price_cents

        status = self.status

        canceled_at: str | Unset = UNSET
        if not isinstance(self.canceled_at, Unset):
            canceled_at = self.canceled_at.isoformat()

        phone_id = self.phone_id

        phone_name = self.phone_name

        phone_nickname = self.phone_nickname

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "cancel_at_period_end": cancel_at_period_end,
                "current_period_end": current_period_end,
                "current_period_start": current_period_start,
                "id": id,
                "organization_id": organization_id,
                "payment_status": payment_status,
                "plan_id": plan_id,
                "plan_interval": plan_interval,
                "plan_name": plan_name,
                "plan_price_cents": plan_price_cents,
                "status": status,
            }
        )
        if canceled_at is not UNSET:
            field_dict["canceled_at"] = canceled_at
        if phone_id is not UNSET:
            field_dict["phone_id"] = phone_id
        if phone_name is not UNSET:
            field_dict["phone_name"] = phone_name
        if phone_nickname is not UNSET:
            field_dict["phone_nickname"] = phone_nickname

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        cancel_at_period_end = d.pop("cancel_at_period_end")

        current_period_end = datetime.datetime.fromisoformat(d.pop("current_period_end"))

        current_period_start = datetime.datetime.fromisoformat(d.pop("current_period_start"))

        id = d.pop("id")

        organization_id = d.pop("organization_id")

        payment_status = d.pop("payment_status")

        plan_id = d.pop("plan_id")

        plan_interval = d.pop("plan_interval")

        plan_name = d.pop("plan_name")

        plan_price_cents = d.pop("plan_price_cents")

        status = d.pop("status")

        _canceled_at = d.pop("canceled_at", UNSET)
        canceled_at: datetime.datetime | Unset
        if isinstance(_canceled_at, Unset):
            canceled_at = UNSET
        else:
            canceled_at = datetime.datetime.fromisoformat(_canceled_at)

        phone_id = d.pop("phone_id", UNSET)

        phone_name = d.pop("phone_name", UNSET)

        phone_nickname = d.pop("phone_nickname", UNSET)

        phone_rental_phone_rental_subscription_response = cls(
            cancel_at_period_end=cancel_at_period_end,
            current_period_end=current_period_end,
            current_period_start=current_period_start,
            id=id,
            organization_id=organization_id,
            payment_status=payment_status,
            plan_id=plan_id,
            plan_interval=plan_interval,
            plan_name=plan_name,
            plan_price_cents=plan_price_cents,
            status=status,
            canceled_at=canceled_at,
            phone_id=phone_id,
            phone_name=phone_name,
            phone_nickname=phone_nickname,
        )

        return phone_rental_phone_rental_subscription_response
