from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.usage_session_sort_spec import UsageSessionSortSpec


T = TypeVar("T", bound="UsageSessionsRequest")


@_attrs_define
class UsageSessionsRequest:
    """
    Attributes:
        end_date (datetime.datetime):
        start_date (datetime.datetime):
        schema (str | Unset): A URL to the JSON Schema for this object.
        allocated_by (list[str] | None | Unset):
        limit (int | Unset):
        offset (int | Unset):
        processed_status_filter (list[str] | None | Unset):
        search (str | Unset):
        session_status_filter (list[str] | None | Unset):
        sort_by (list[UsageSessionSortSpec] | None | Unset):
        workflow_id (str | Unset):
    """

    end_date: datetime.datetime
    start_date: datetime.datetime
    schema: str | Unset = UNSET
    allocated_by: list[str] | None | Unset = UNSET
    limit: int | Unset = UNSET
    offset: int | Unset = UNSET
    processed_status_filter: list[str] | None | Unset = UNSET
    search: str | Unset = UNSET
    session_status_filter: list[str] | None | Unset = UNSET
    sort_by: list[UsageSessionSortSpec] | None | Unset = UNSET
    workflow_id: str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        end_date = self.end_date.isoformat()

        start_date = self.start_date.isoformat()

        schema = self.schema

        allocated_by: list[str] | None | Unset
        if isinstance(self.allocated_by, Unset):
            allocated_by = UNSET
        elif isinstance(self.allocated_by, list):
            allocated_by = self.allocated_by

        else:
            allocated_by = self.allocated_by

        limit = self.limit

        offset = self.offset

        processed_status_filter: list[str] | None | Unset
        if isinstance(self.processed_status_filter, Unset):
            processed_status_filter = UNSET
        elif isinstance(self.processed_status_filter, list):
            processed_status_filter = self.processed_status_filter

        else:
            processed_status_filter = self.processed_status_filter

        search = self.search

        session_status_filter: list[str] | None | Unset
        if isinstance(self.session_status_filter, Unset):
            session_status_filter = UNSET
        elif isinstance(self.session_status_filter, list):
            session_status_filter = self.session_status_filter

        else:
            session_status_filter = self.session_status_filter

        sort_by: list[dict[str, Any]] | None | Unset
        if isinstance(self.sort_by, Unset):
            sort_by = UNSET
        elif isinstance(self.sort_by, list):
            sort_by = []
            for sort_by_type_0_item_data in self.sort_by:
                sort_by_type_0_item = sort_by_type_0_item_data.to_dict()
                sort_by.append(sort_by_type_0_item)

        else:
            sort_by = self.sort_by

        workflow_id = self.workflow_id

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "end_date": end_date,
                "start_date": start_date,
            }
        )
        if schema is not UNSET:
            field_dict["$schema"] = schema
        if allocated_by is not UNSET:
            field_dict["allocated_by"] = allocated_by
        if limit is not UNSET:
            field_dict["limit"] = limit
        if offset is not UNSET:
            field_dict["offset"] = offset
        if processed_status_filter is not UNSET:
            field_dict["processed_status_filter"] = processed_status_filter
        if search is not UNSET:
            field_dict["search"] = search
        if session_status_filter is not UNSET:
            field_dict["session_status_filter"] = session_status_filter
        if sort_by is not UNSET:
            field_dict["sort_by"] = sort_by
        if workflow_id is not UNSET:
            field_dict["workflow_id"] = workflow_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.usage_session_sort_spec import UsageSessionSortSpec

        d = dict(src_dict)
        end_date = datetime.datetime.fromisoformat(d.pop("end_date"))

        start_date = datetime.datetime.fromisoformat(d.pop("start_date"))

        schema = d.pop("$schema", UNSET)

        def _parse_allocated_by(data: object) -> list[str] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                allocated_by_type_0 = cast(list[str], data)

                return allocated_by_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[str] | None | Unset, data)

        allocated_by = _parse_allocated_by(d.pop("allocated_by", UNSET))

        limit = d.pop("limit", UNSET)

        offset = d.pop("offset", UNSET)

        def _parse_processed_status_filter(data: object) -> list[str] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                processed_status_filter_type_0 = cast(list[str], data)

                return processed_status_filter_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[str] | None | Unset, data)

        processed_status_filter = _parse_processed_status_filter(d.pop("processed_status_filter", UNSET))

        search = d.pop("search", UNSET)

        def _parse_session_status_filter(data: object) -> list[str] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                session_status_filter_type_0 = cast(list[str], data)

                return session_status_filter_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[str] | None | Unset, data)

        session_status_filter = _parse_session_status_filter(d.pop("session_status_filter", UNSET))

        def _parse_sort_by(data: object) -> list[UsageSessionSortSpec] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                sort_by_type_0 = []
                _sort_by_type_0 = data
                for sort_by_type_0_item_data in _sort_by_type_0:
                    sort_by_type_0_item = UsageSessionSortSpec.from_dict(sort_by_type_0_item_data)

                    sort_by_type_0.append(sort_by_type_0_item)

                return sort_by_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[UsageSessionSortSpec] | None | Unset, data)

        sort_by = _parse_sort_by(d.pop("sort_by", UNSET))

        workflow_id = d.pop("workflow_id", UNSET)

        usage_sessions_request = cls(
            end_date=end_date,
            start_date=start_date,
            schema=schema,
            allocated_by=allocated_by,
            limit=limit,
            offset=offset,
            processed_status_filter=processed_status_filter,
            search=search,
            session_status_filter=session_status_filter,
            sort_by=sort_by,
            workflow_id=workflow_id,
        )

        return usage_sessions_request
