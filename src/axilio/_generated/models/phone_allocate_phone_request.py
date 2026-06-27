from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="PhoneAllocatePhoneRequest")


@_attrs_define
class PhoneAllocatePhoneRequest:
    """
    Attributes:
        phone_type (str):
        schema (str | Unset): A URL to the JSON Schema for this object.
        phone_id (str | Unset):
        workflow_id (str | Unset):
    """

    phone_type: str
    schema: str | Unset = UNSET
    phone_id: str | Unset = UNSET
    workflow_id: str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        phone_type = self.phone_type

        schema = self.schema

        phone_id = self.phone_id

        workflow_id = self.workflow_id

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "phone_type": phone_type,
            }
        )
        if schema is not UNSET:
            field_dict["$schema"] = schema
        if phone_id is not UNSET:
            field_dict["phone_id"] = phone_id
        if workflow_id is not UNSET:
            field_dict["workflow_id"] = workflow_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        phone_type = d.pop("phone_type")

        schema = d.pop("$schema", UNSET)

        phone_id = d.pop("phone_id", UNSET)

        workflow_id = d.pop("workflow_id", UNSET)

        phone_allocate_phone_request = cls(
            phone_type=phone_type,
            schema=schema,
            phone_id=phone_id,
            workflow_id=workflow_id,
        )

        return phone_allocate_phone_request
