from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="PhoneAllocationStatusResponse")


@_attrs_define
class PhoneAllocationStatusResponse:
    """
    Attributes:
        allocated (bool):
        workflow_id (str):
        schema (str | Unset): A URL to the JSON Schema for this object.
        phone_id (str | Unset):
        reason (str | Unset):
        session_id (str | Unset):
        workflow_started_at (datetime.datetime | Unset):
    """

    allocated: bool
    workflow_id: str
    schema: str | Unset = UNSET
    phone_id: str | Unset = UNSET
    reason: str | Unset = UNSET
    session_id: str | Unset = UNSET
    workflow_started_at: datetime.datetime | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        allocated = self.allocated

        workflow_id = self.workflow_id

        schema = self.schema

        phone_id = self.phone_id

        reason = self.reason

        session_id = self.session_id

        workflow_started_at: str | Unset = UNSET
        if not isinstance(self.workflow_started_at, Unset):
            workflow_started_at = self.workflow_started_at.isoformat()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "allocated": allocated,
                "workflow_id": workflow_id,
            }
        )
        if schema is not UNSET:
            field_dict["$schema"] = schema
        if phone_id is not UNSET:
            field_dict["phone_id"] = phone_id
        if reason is not UNSET:
            field_dict["reason"] = reason
        if session_id is not UNSET:
            field_dict["session_id"] = session_id
        if workflow_started_at is not UNSET:
            field_dict["workflow_started_at"] = workflow_started_at

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        allocated = d.pop("allocated")

        workflow_id = d.pop("workflow_id")

        schema = d.pop("$schema", UNSET)

        phone_id = d.pop("phone_id", UNSET)

        reason = d.pop("reason", UNSET)

        session_id = d.pop("session_id", UNSET)

        _workflow_started_at = d.pop("workflow_started_at", UNSET)
        workflow_started_at: datetime.datetime | Unset
        if isinstance(_workflow_started_at, Unset):
            workflow_started_at = UNSET
        else:
            workflow_started_at = datetime.datetime.fromisoformat(_workflow_started_at)

        phone_allocation_status_response = cls(
            allocated=allocated,
            workflow_id=workflow_id,
            schema=schema,
            phone_id=phone_id,
            reason=reason,
            session_id=session_id,
            workflow_started_at=workflow_started_at,
        )

        return phone_allocation_status_response
