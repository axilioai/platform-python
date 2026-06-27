from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="WorkflowWorkflowCreateRequest")


@_attrs_define
class WorkflowWorkflowCreateRequest:
    """
    Attributes:
        name (str):
        schema (str | Unset): A URL to the JSON Schema for this object.
        goal (str | Unset):
        ocr_engine (str | Unset):
        platform (str | Unset):
    """

    name: str
    schema: str | Unset = UNSET
    goal: str | Unset = UNSET
    ocr_engine: str | Unset = UNSET
    platform: str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        schema = self.schema

        goal = self.goal

        ocr_engine = self.ocr_engine

        platform = self.platform

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "name": name,
            }
        )
        if schema is not UNSET:
            field_dict["$schema"] = schema
        if goal is not UNSET:
            field_dict["goal"] = goal
        if ocr_engine is not UNSET:
            field_dict["ocr_engine"] = ocr_engine
        if platform is not UNSET:
            field_dict["platform"] = platform

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        schema = d.pop("$schema", UNSET)

        goal = d.pop("goal", UNSET)

        ocr_engine = d.pop("ocr_engine", UNSET)

        platform = d.pop("platform", UNSET)

        workflow_workflow_create_request = cls(
            name=name,
            schema=schema,
            goal=goal,
            ocr_engine=ocr_engine,
            platform=platform,
        )

        return workflow_workflow_create_request
