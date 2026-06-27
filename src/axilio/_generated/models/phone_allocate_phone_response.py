from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="PhoneAllocatePhoneResponse")


@_attrs_define
class PhoneAllocatePhoneResponse:
    """
    Attributes:
        phone_id (str):
        session_id (str):
        workflow_started_at (datetime.datetime):
        schema (str | Unset): A URL to the JSON Schema for this object.
        region (str | Unset):
    """

    phone_id: str
    session_id: str
    workflow_started_at: datetime.datetime
    schema: str | Unset = UNSET
    region: str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        phone_id = self.phone_id

        session_id = self.session_id

        workflow_started_at = self.workflow_started_at.isoformat()

        schema = self.schema

        region = self.region

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "phone_id": phone_id,
                "session_id": session_id,
                "workflow_started_at": workflow_started_at,
            }
        )
        if schema is not UNSET:
            field_dict["$schema"] = schema
        if region is not UNSET:
            field_dict["region"] = region

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        phone_id = d.pop("phone_id")

        session_id = d.pop("session_id")

        workflow_started_at = datetime.datetime.fromisoformat(d.pop("workflow_started_at"))

        schema = d.pop("$schema", UNSET)

        region = d.pop("region", UNSET)

        phone_allocate_phone_response = cls(
            phone_id=phone_id,
            session_id=session_id,
            workflow_started_at=workflow_started_at,
            schema=schema,
            region=region,
        )

        return phone_allocate_phone_response
