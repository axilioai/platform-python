from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="WorkflowWorkflowRunUpdateRequest")


@_attrs_define
class WorkflowWorkflowRunUpdateRequest:
    """
    Attributes:
        schema (str | Unset): A URL to the JSON Schema for this object.
        last_run_at (datetime.datetime | Unset):
    """

    schema: str | Unset = UNSET
    last_run_at: datetime.datetime | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        schema = self.schema

        last_run_at: str | Unset = UNSET
        if not isinstance(self.last_run_at, Unset):
            last_run_at = self.last_run_at.isoformat()

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if schema is not UNSET:
            field_dict["$schema"] = schema
        if last_run_at is not UNSET:
            field_dict["last_run_at"] = last_run_at

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        schema = d.pop("$schema", UNSET)

        _last_run_at = d.pop("last_run_at", UNSET)
        last_run_at: datetime.datetime | Unset
        if isinstance(_last_run_at, Unset):
            last_run_at = UNSET
        else:
            last_run_at = datetime.datetime.fromisoformat(_last_run_at)

        workflow_workflow_run_update_request = cls(
            schema=schema,
            last_run_at=last_run_at,
        )

        return workflow_workflow_run_update_request
