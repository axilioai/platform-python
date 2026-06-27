from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="RunRunEventSummary")


@_attrs_define
class RunRunEventSummary:
    """
    Attributes:
        session_id (str):
        timestamp (str):
        type_ (str):
        body (Any | Unset):
    """

    session_id: str
    timestamp: str
    type_: str
    body: Any | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        session_id = self.session_id

        timestamp = self.timestamp

        type_ = self.type_

        body = self.body

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "session_id": session_id,
                "timestamp": timestamp,
                "type": type_,
            }
        )
        if body is not UNSET:
            field_dict["body"] = body

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        session_id = d.pop("session_id")

        timestamp = d.pop("timestamp")

        type_ = d.pop("type")

        body = d.pop("body", UNSET)

        run_run_event_summary = cls(
            session_id=session_id,
            timestamp=timestamp,
            type_=type_,
            body=body,
        )

        return run_run_event_summary
