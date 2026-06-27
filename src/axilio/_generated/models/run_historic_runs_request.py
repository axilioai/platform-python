from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="RunHistoricRunsRequest")


@_attrs_define
class RunHistoricRunsRequest:
    """
    Attributes:
        end_date (datetime.datetime):
        limit (int):
        offset (int):
        start_date (datetime.datetime):
        schema (str | Unset): A URL to the JSON Schema for this object.
        search (str | Unset):
        status_filter (list[str] | None | Unset):
        workflow_id (str | Unset):
    """

    end_date: datetime.datetime
    limit: int
    offset: int
    start_date: datetime.datetime
    schema: str | Unset = UNSET
    search: str | Unset = UNSET
    status_filter: list[str] | None | Unset = UNSET
    workflow_id: str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        end_date = self.end_date.isoformat()

        limit = self.limit

        offset = self.offset

        start_date = self.start_date.isoformat()

        schema = self.schema

        search = self.search

        status_filter: list[str] | None | Unset
        if isinstance(self.status_filter, Unset):
            status_filter = UNSET
        elif isinstance(self.status_filter, list):
            status_filter = self.status_filter

        else:
            status_filter = self.status_filter

        workflow_id = self.workflow_id

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "end_date": end_date,
                "limit": limit,
                "offset": offset,
                "start_date": start_date,
            }
        )
        if schema is not UNSET:
            field_dict["$schema"] = schema
        if search is not UNSET:
            field_dict["search"] = search
        if status_filter is not UNSET:
            field_dict["status_filter"] = status_filter
        if workflow_id is not UNSET:
            field_dict["workflow_id"] = workflow_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        end_date = datetime.datetime.fromisoformat(d.pop("end_date"))

        limit = d.pop("limit")

        offset = d.pop("offset")

        start_date = datetime.datetime.fromisoformat(d.pop("start_date"))

        schema = d.pop("$schema", UNSET)

        search = d.pop("search", UNSET)

        def _parse_status_filter(data: object) -> list[str] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                status_filter_type_0 = cast(list[str], data)

                return status_filter_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[str] | None | Unset, data)

        status_filter = _parse_status_filter(d.pop("status_filter", UNSET))

        workflow_id = d.pop("workflow_id", UNSET)

        run_historic_runs_request = cls(
            end_date=end_date,
            limit=limit,
            offset=offset,
            start_date=start_date,
            schema=schema,
            search=search,
            status_filter=status_filter,
            workflow_id=workflow_id,
        )

        return run_historic_runs_request
