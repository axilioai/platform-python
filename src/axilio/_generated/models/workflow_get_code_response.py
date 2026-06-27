from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="WorkflowGetCodeResponse")


@_attrs_define
class WorkflowGetCodeResponse:
    """
    Attributes:
        revision (int):
        revision_id (None | str):
        source (str):
        updated_at (datetime.datetime):
        schema (str | Unset): A URL to the JSON Schema for this object.
    """

    revision: int
    revision_id: None | str
    source: str
    updated_at: datetime.datetime
    schema: str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        revision = self.revision

        revision_id: None | str
        revision_id = self.revision_id

        source = self.source

        updated_at = self.updated_at.isoformat()

        schema = self.schema

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "revision": revision,
                "revision_id": revision_id,
                "source": source,
                "updated_at": updated_at,
            }
        )
        if schema is not UNSET:
            field_dict["$schema"] = schema

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        revision = d.pop("revision")

        def _parse_revision_id(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        revision_id = _parse_revision_id(d.pop("revision_id"))

        source = d.pop("source")

        updated_at = datetime.datetime.fromisoformat(d.pop("updated_at"))

        schema = d.pop("$schema", UNSET)

        workflow_get_code_response = cls(
            revision=revision,
            revision_id=revision_id,
            source=source,
            updated_at=updated_at,
            schema=schema,
        )

        return workflow_get_code_response
