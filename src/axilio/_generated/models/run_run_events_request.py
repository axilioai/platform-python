from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="RunRunEventsRequest")


@_attrs_define
class RunRunEventsRequest:
    """
    Attributes:
        limit (int):
        offset (int):
        session_id (str):
        schema (str | Unset): A URL to the JSON Schema for this object.
        event_types (list[str] | None | Unset):
    """

    limit: int
    offset: int
    session_id: str
    schema: str | Unset = UNSET
    event_types: list[str] | None | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        limit = self.limit

        offset = self.offset

        session_id = self.session_id

        schema = self.schema

        event_types: list[str] | None | Unset
        if isinstance(self.event_types, Unset):
            event_types = UNSET
        elif isinstance(self.event_types, list):
            event_types = self.event_types

        else:
            event_types = self.event_types

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "limit": limit,
                "offset": offset,
                "session_id": session_id,
            }
        )
        if schema is not UNSET:
            field_dict["$schema"] = schema
        if event_types is not UNSET:
            field_dict["event_types"] = event_types

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        limit = d.pop("limit")

        offset = d.pop("offset")

        session_id = d.pop("session_id")

        schema = d.pop("$schema", UNSET)

        def _parse_event_types(data: object) -> list[str] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                event_types_type_0 = cast(list[str], data)

                return event_types_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[str] | None | Unset, data)

        event_types = _parse_event_types(d.pop("event_types", UNSET))

        run_run_events_request = cls(
            limit=limit,
            offset=offset,
            session_id=session_id,
            schema=schema,
            event_types=event_types,
        )

        return run_run_events_request
