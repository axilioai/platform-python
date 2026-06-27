from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="PhoneSessionDetailResponse")


@_attrs_define
class PhoneSessionDetailResponse:
    """
    Attributes:
        allocated_at (str):
        is_dedicated_phone (bool):
        phone_id (str):
        phone_status (str):
        recording_status (str):
        session_id (str):
        source (str):
        status (str):
        schema (str | Unset): A URL to the JSON Schema for this object.
        allocated_by (str | Unset):
        deallocated_at (str | Unset):
        location (str | Unset):
        model_name (str | Unset):
        nickname (str | Unset):
        phone_name (str | Unset):
        phone_type (str | Unset):
        recording_url (str | Unset):
        workflow_id (str | Unset):
        workflow_name (str | Unset):
    """

    allocated_at: str
    is_dedicated_phone: bool
    phone_id: str
    phone_status: str
    recording_status: str
    session_id: str
    source: str
    status: str
    schema: str | Unset = UNSET
    allocated_by: str | Unset = UNSET
    deallocated_at: str | Unset = UNSET
    location: str | Unset = UNSET
    model_name: str | Unset = UNSET
    nickname: str | Unset = UNSET
    phone_name: str | Unset = UNSET
    phone_type: str | Unset = UNSET
    recording_url: str | Unset = UNSET
    workflow_id: str | Unset = UNSET
    workflow_name: str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        allocated_at = self.allocated_at

        is_dedicated_phone = self.is_dedicated_phone

        phone_id = self.phone_id

        phone_status = self.phone_status

        recording_status = self.recording_status

        session_id = self.session_id

        source = self.source

        status = self.status

        schema = self.schema

        allocated_by = self.allocated_by

        deallocated_at = self.deallocated_at

        location = self.location

        model_name = self.model_name

        nickname = self.nickname

        phone_name = self.phone_name

        phone_type = self.phone_type

        recording_url = self.recording_url

        workflow_id = self.workflow_id

        workflow_name = self.workflow_name

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "allocated_at": allocated_at,
                "is_dedicated_phone": is_dedicated_phone,
                "phone_id": phone_id,
                "phone_status": phone_status,
                "recording_status": recording_status,
                "session_id": session_id,
                "source": source,
                "status": status,
            }
        )
        if schema is not UNSET:
            field_dict["$schema"] = schema
        if allocated_by is not UNSET:
            field_dict["allocated_by"] = allocated_by
        if deallocated_at is not UNSET:
            field_dict["deallocated_at"] = deallocated_at
        if location is not UNSET:
            field_dict["location"] = location
        if model_name is not UNSET:
            field_dict["model_name"] = model_name
        if nickname is not UNSET:
            field_dict["nickname"] = nickname
        if phone_name is not UNSET:
            field_dict["phone_name"] = phone_name
        if phone_type is not UNSET:
            field_dict["phone_type"] = phone_type
        if recording_url is not UNSET:
            field_dict["recording_url"] = recording_url
        if workflow_id is not UNSET:
            field_dict["workflow_id"] = workflow_id
        if workflow_name is not UNSET:
            field_dict["workflow_name"] = workflow_name

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        allocated_at = d.pop("allocated_at")

        is_dedicated_phone = d.pop("is_dedicated_phone")

        phone_id = d.pop("phone_id")

        phone_status = d.pop("phone_status")

        recording_status = d.pop("recording_status")

        session_id = d.pop("session_id")

        source = d.pop("source")

        status = d.pop("status")

        schema = d.pop("$schema", UNSET)

        allocated_by = d.pop("allocated_by", UNSET)

        deallocated_at = d.pop("deallocated_at", UNSET)

        location = d.pop("location", UNSET)

        model_name = d.pop("model_name", UNSET)

        nickname = d.pop("nickname", UNSET)

        phone_name = d.pop("phone_name", UNSET)

        phone_type = d.pop("phone_type", UNSET)

        recording_url = d.pop("recording_url", UNSET)

        workflow_id = d.pop("workflow_id", UNSET)

        workflow_name = d.pop("workflow_name", UNSET)

        phone_session_detail_response = cls(
            allocated_at=allocated_at,
            is_dedicated_phone=is_dedicated_phone,
            phone_id=phone_id,
            phone_status=phone_status,
            recording_status=recording_status,
            session_id=session_id,
            source=source,
            status=status,
            schema=schema,
            allocated_by=allocated_by,
            deallocated_at=deallocated_at,
            location=location,
            model_name=model_name,
            nickname=nickname,
            phone_name=phone_name,
            phone_type=phone_type,
            recording_url=recording_url,
            workflow_id=workflow_id,
            workflow_name=workflow_name,
        )

        return phone_session_detail_response
