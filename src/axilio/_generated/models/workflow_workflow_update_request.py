from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="WorkflowWorkflowUpdateRequest")


@_attrs_define
class WorkflowWorkflowUpdateRequest:
    """
    Attributes:
        schema (str | Unset): A URL to the JSON Schema for this object.
        name (str | Unset):
        ocr_engine (str | Unset):
        platform (str | Unset):
        status (str | Unset):
    """

    schema: str | Unset = UNSET
    name: str | Unset = UNSET
    ocr_engine: str | Unset = UNSET
    platform: str | Unset = UNSET
    status: str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        schema = self.schema

        name = self.name

        ocr_engine = self.ocr_engine

        platform = self.platform

        status = self.status

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if schema is not UNSET:
            field_dict["$schema"] = schema
        if name is not UNSET:
            field_dict["name"] = name
        if ocr_engine is not UNSET:
            field_dict["ocr_engine"] = ocr_engine
        if platform is not UNSET:
            field_dict["platform"] = platform
        if status is not UNSET:
            field_dict["status"] = status

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        schema = d.pop("$schema", UNSET)

        name = d.pop("name", UNSET)

        ocr_engine = d.pop("ocr_engine", UNSET)

        platform = d.pop("platform", UNSET)

        status = d.pop("status", UNSET)

        workflow_workflow_update_request = cls(
            schema=schema,
            name=name,
            ocr_engine=ocr_engine,
            platform=platform,
            status=status,
        )

        return workflow_workflow_update_request
