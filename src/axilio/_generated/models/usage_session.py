from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.usage_session_session_metadata import UsageSessionSessionMetadata


T = TypeVar("T", bound="UsageSession")


@_attrs_define
class UsageSession:
    """
    Attributes:
        cost_microdollars (int):
        inference_cost_microdollars (int):
        is_dedicated_phone (bool):
        phone_id (str):
        session_id (str):
        total_cost_microdollars (int):
        workflow_id (str):
        allocated_at (str | Unset):
        allocated_by (str | Unset):
        billing_plan_id (str | Unset):
        deallocated_at (str | Unset):
        duration_seconds (int | Unset):
        processed_status (str | Unset):
        session_metadata (UsageSessionSessionMetadata | Unset):
        session_status (str | Unset):
    """

    cost_microdollars: int
    inference_cost_microdollars: int
    is_dedicated_phone: bool
    phone_id: str
    session_id: str
    total_cost_microdollars: int
    workflow_id: str
    allocated_at: str | Unset = UNSET
    allocated_by: str | Unset = UNSET
    billing_plan_id: str | Unset = UNSET
    deallocated_at: str | Unset = UNSET
    duration_seconds: int | Unset = UNSET
    processed_status: str | Unset = UNSET
    session_metadata: UsageSessionSessionMetadata | Unset = UNSET
    session_status: str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        cost_microdollars = self.cost_microdollars

        inference_cost_microdollars = self.inference_cost_microdollars

        is_dedicated_phone = self.is_dedicated_phone

        phone_id = self.phone_id

        session_id = self.session_id

        total_cost_microdollars = self.total_cost_microdollars

        workflow_id = self.workflow_id

        allocated_at = self.allocated_at

        allocated_by = self.allocated_by

        billing_plan_id = self.billing_plan_id

        deallocated_at = self.deallocated_at

        duration_seconds = self.duration_seconds

        processed_status = self.processed_status

        session_metadata: dict[str, Any] | Unset = UNSET
        if not isinstance(self.session_metadata, Unset):
            session_metadata = self.session_metadata.to_dict()

        session_status = self.session_status

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "cost_microdollars": cost_microdollars,
                "inference_cost_microdollars": inference_cost_microdollars,
                "is_dedicated_phone": is_dedicated_phone,
                "phone_id": phone_id,
                "session_id": session_id,
                "total_cost_microdollars": total_cost_microdollars,
                "workflow_id": workflow_id,
            }
        )
        if allocated_at is not UNSET:
            field_dict["allocated_at"] = allocated_at
        if allocated_by is not UNSET:
            field_dict["allocated_by"] = allocated_by
        if billing_plan_id is not UNSET:
            field_dict["billing_plan_id"] = billing_plan_id
        if deallocated_at is not UNSET:
            field_dict["deallocated_at"] = deallocated_at
        if duration_seconds is not UNSET:
            field_dict["duration_seconds"] = duration_seconds
        if processed_status is not UNSET:
            field_dict["processed_status"] = processed_status
        if session_metadata is not UNSET:
            field_dict["session_metadata"] = session_metadata
        if session_status is not UNSET:
            field_dict["session_status"] = session_status

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.usage_session_session_metadata import UsageSessionSessionMetadata

        d = dict(src_dict)
        cost_microdollars = d.pop("cost_microdollars")

        inference_cost_microdollars = d.pop("inference_cost_microdollars")

        is_dedicated_phone = d.pop("is_dedicated_phone")

        phone_id = d.pop("phone_id")

        session_id = d.pop("session_id")

        total_cost_microdollars = d.pop("total_cost_microdollars")

        workflow_id = d.pop("workflow_id")

        allocated_at = d.pop("allocated_at", UNSET)

        allocated_by = d.pop("allocated_by", UNSET)

        billing_plan_id = d.pop("billing_plan_id", UNSET)

        deallocated_at = d.pop("deallocated_at", UNSET)

        duration_seconds = d.pop("duration_seconds", UNSET)

        processed_status = d.pop("processed_status", UNSET)

        _session_metadata = d.pop("session_metadata", UNSET)
        session_metadata: UsageSessionSessionMetadata | Unset
        if isinstance(_session_metadata, Unset):
            session_metadata = UNSET
        else:
            session_metadata = UsageSessionSessionMetadata.from_dict(_session_metadata)

        session_status = d.pop("session_status", UNSET)

        usage_session = cls(
            cost_microdollars=cost_microdollars,
            inference_cost_microdollars=inference_cost_microdollars,
            is_dedicated_phone=is_dedicated_phone,
            phone_id=phone_id,
            session_id=session_id,
            total_cost_microdollars=total_cost_microdollars,
            workflow_id=workflow_id,
            allocated_at=allocated_at,
            allocated_by=allocated_by,
            billing_plan_id=billing_plan_id,
            deallocated_at=deallocated_at,
            duration_seconds=duration_seconds,
            processed_status=processed_status,
            session_metadata=session_metadata,
            session_status=session_status,
        )

        return usage_session
