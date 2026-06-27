from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="PhoneConnectPhoneRequest")


@_attrs_define
class PhoneConnectPhoneRequest:
    """
    Attributes:
        phone_id (str):
        workflow_id (str):
        schema (str | Unset): A URL to the JSON Schema for this object.
    """

    phone_id: str
    workflow_id: str
    schema: str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        phone_id = self.phone_id

        workflow_id = self.workflow_id

        schema = self.schema

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "phone_id": phone_id,
                "workflow_id": workflow_id,
            }
        )
        if schema is not UNSET:
            field_dict["$schema"] = schema

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        phone_id = d.pop("phone_id")

        workflow_id = d.pop("workflow_id")

        schema = d.pop("$schema", UNSET)

        phone_connect_phone_request = cls(
            phone_id=phone_id,
            workflow_id=workflow_id,
            schema=schema,
        )

        return phone_connect_phone_request
