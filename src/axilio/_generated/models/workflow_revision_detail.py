from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="WorkflowRevisionDetail")


@_attrs_define
class WorkflowRevisionDetail:
    """
    Attributes:
        author_user_id (str):
        bytes_ (int):
        code_source (str):
        created_at (datetime.datetime):
        id (str):
        message (None | str):
        revision (int):
        sha256 (str):
        schema (str | Unset): A URL to the JSON Schema for this object.
    """

    author_user_id: str
    bytes_: int
    code_source: str
    created_at: datetime.datetime
    id: str
    message: None | str
    revision: int
    sha256: str
    schema: str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        author_user_id = self.author_user_id

        bytes_ = self.bytes_

        code_source = self.code_source

        created_at = self.created_at.isoformat()

        id = self.id

        message: None | str
        message = self.message

        revision = self.revision

        sha256 = self.sha256

        schema = self.schema

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "author_user_id": author_user_id,
                "bytes": bytes_,
                "code_source": code_source,
                "created_at": created_at,
                "id": id,
                "message": message,
                "revision": revision,
                "sha256": sha256,
            }
        )
        if schema is not UNSET:
            field_dict["$schema"] = schema

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        author_user_id = d.pop("author_user_id")

        bytes_ = d.pop("bytes")

        code_source = d.pop("code_source")

        created_at = datetime.datetime.fromisoformat(d.pop("created_at"))

        id = d.pop("id")

        def _parse_message(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        message = _parse_message(d.pop("message"))

        revision = d.pop("revision")

        sha256 = d.pop("sha256")

        schema = d.pop("$schema", UNSET)

        workflow_revision_detail = cls(
            author_user_id=author_user_id,
            bytes_=bytes_,
            code_source=code_source,
            created_at=created_at,
            id=id,
            message=message,
            revision=revision,
            sha256=sha256,
            schema=schema,
        )

        return workflow_revision_detail
