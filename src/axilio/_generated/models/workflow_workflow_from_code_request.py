from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="WorkflowWorkflowFromCodeRequest")


@_attrs_define
class WorkflowWorkflowFromCodeRequest:
    """
    Attributes:
        code_source (str):
        name (str):
        schema (str | Unset): A URL to the JSON Schema for this object.
        goal (str | Unset):
        platform (str | Unset):
    """

    code_source: str
    name: str
    schema: str | Unset = UNSET
    goal: str | Unset = UNSET
    platform: str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        code_source = self.code_source

        name = self.name

        schema = self.schema

        goal = self.goal

        platform = self.platform

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "code_source": code_source,
                "name": name,
            }
        )
        if schema is not UNSET:
            field_dict["$schema"] = schema
        if goal is not UNSET:
            field_dict["goal"] = goal
        if platform is not UNSET:
            field_dict["platform"] = platform

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        code_source = d.pop("code_source")

        name = d.pop("name")

        schema = d.pop("$schema", UNSET)

        goal = d.pop("goal", UNSET)

        platform = d.pop("platform", UNSET)

        workflow_workflow_from_code_request = cls(
            code_source=code_source,
            name=name,
            schema=schema,
            goal=goal,
            platform=platform,
        )

        return workflow_workflow_from_code_request
