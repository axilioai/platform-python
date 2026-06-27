from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="PhoneDeallocatePhoneResponse")


@_attrs_define
class PhoneDeallocatePhoneResponse:
    """
    Attributes:
        phone_id (str):
        session_id (str):
        workflow_id (str):
        schema (str | Unset): A URL to the JSON Schema for this object.
        deallocated_at (datetime.datetime | Unset):
    """

    phone_id: str
    session_id: str
    workflow_id: str
    schema: str | Unset = UNSET
    deallocated_at: datetime.datetime | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        phone_id = self.phone_id

        session_id = self.session_id

        workflow_id = self.workflow_id

        schema = self.schema

        deallocated_at: str | Unset = UNSET
        if not isinstance(self.deallocated_at, Unset):
            deallocated_at = self.deallocated_at.isoformat()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "phone_id": phone_id,
                "session_id": session_id,
                "workflow_id": workflow_id,
            }
        )
        if schema is not UNSET:
            field_dict["$schema"] = schema
        if deallocated_at is not UNSET:
            field_dict["deallocated_at"] = deallocated_at

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        phone_id = d.pop("phone_id")

        session_id = d.pop("session_id")

        workflow_id = d.pop("workflow_id")

        schema = d.pop("$schema", UNSET)

        _deallocated_at = d.pop("deallocated_at", UNSET)
        deallocated_at: datetime.datetime | Unset
        if isinstance(_deallocated_at, Unset):
            deallocated_at = UNSET
        else:
            deallocated_at = datetime.datetime.fromisoformat(_deallocated_at)

        phone_deallocate_phone_response = cls(
            phone_id=phone_id,
            session_id=session_id,
            workflow_id=workflow_id,
            schema=schema,
            deallocated_at=deallocated_at,
        )

        return phone_deallocate_phone_response
