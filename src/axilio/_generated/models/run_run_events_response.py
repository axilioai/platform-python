from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.run_run_event_summary import RunRunEventSummary


T = TypeVar("T", bound="RunRunEventsResponse")


@_attrs_define
class RunRunEventsResponse:
    """
    Attributes:
        events (list[RunRunEventSummary] | None):
        limit (int):
        offset (int):
        total (int):
        schema (str | Unset): A URL to the JSON Schema for this object.
    """

    events: list[RunRunEventSummary] | None
    limit: int
    offset: int
    total: int
    schema: str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        events: list[dict[str, Any]] | None
        if isinstance(self.events, list):
            events = []
            for events_type_0_item_data in self.events:
                events_type_0_item = events_type_0_item_data.to_dict()
                events.append(events_type_0_item)

        else:
            events = self.events

        limit = self.limit

        offset = self.offset

        total = self.total

        schema = self.schema

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "events": events,
                "limit": limit,
                "offset": offset,
                "total": total,
            }
        )
        if schema is not UNSET:
            field_dict["$schema"] = schema

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.run_run_event_summary import RunRunEventSummary

        d = dict(src_dict)

        def _parse_events(data: object) -> list[RunRunEventSummary] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                events_type_0 = []
                _events_type_0 = data
                for events_type_0_item_data in _events_type_0:
                    events_type_0_item = RunRunEventSummary.from_dict(events_type_0_item_data)

                    events_type_0.append(events_type_0_item)

                return events_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[RunRunEventSummary] | None, data)

        events = _parse_events(d.pop("events"))

        limit = d.pop("limit")

        offset = d.pop("offset")

        total = d.pop("total")

        schema = d.pop("$schema", UNSET)

        run_run_events_response = cls(
            events=events,
            limit=limit,
            offset=offset,
            total=total,
            schema=schema,
        )

        return run_run_events_response
