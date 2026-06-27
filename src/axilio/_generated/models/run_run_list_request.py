from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.run_run_sort_spec import RunRunSortSpec


T = TypeVar("T", bound="RunRunListRequest")


@_attrs_define
class RunRunListRequest:
    """
    Attributes:
        limit (int):
        offset (int):
        schema (str | Unset): A URL to the JSON Schema for this object.
        search (str | Unset):
        sort_by (list[RunRunSortSpec] | None | Unset):
        status_filter (list[str] | None | Unset):
        trigger_filter (list[str] | None | Unset):
        workflow_id (str | Unset):
    """

    limit: int
    offset: int
    schema: str | Unset = UNSET
    search: str | Unset = UNSET
    sort_by: list[RunRunSortSpec] | None | Unset = UNSET
    status_filter: list[str] | None | Unset = UNSET
    trigger_filter: list[str] | None | Unset = UNSET
    workflow_id: str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        limit = self.limit

        offset = self.offset

        schema = self.schema

        search = self.search

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

        status_filter: list[str] | None | Unset
        if isinstance(self.status_filter, Unset):
            status_filter = UNSET
        elif isinstance(self.status_filter, list):
            status_filter = self.status_filter

        else:
            status_filter = self.status_filter

        trigger_filter: list[str] | None | Unset
        if isinstance(self.trigger_filter, Unset):
            trigger_filter = UNSET
        elif isinstance(self.trigger_filter, list):
            trigger_filter = self.trigger_filter

        else:
            trigger_filter = self.trigger_filter

        workflow_id = self.workflow_id

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "limit": limit,
                "offset": offset,
            }
        )
        if schema is not UNSET:
            field_dict["$schema"] = schema
        if search is not UNSET:
            field_dict["search"] = search
        if sort_by is not UNSET:
            field_dict["sort_by"] = sort_by
        if status_filter is not UNSET:
            field_dict["status_filter"] = status_filter
        if trigger_filter is not UNSET:
            field_dict["trigger_filter"] = trigger_filter
        if workflow_id is not UNSET:
            field_dict["workflow_id"] = workflow_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.run_run_sort_spec import RunRunSortSpec

        d = dict(src_dict)
        limit = d.pop("limit")

        offset = d.pop("offset")

        schema = d.pop("$schema", UNSET)

        search = d.pop("search", UNSET)

        def _parse_sort_by(data: object) -> list[RunRunSortSpec] | None | Unset:
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
                    sort_by_type_0_item = RunRunSortSpec.from_dict(sort_by_type_0_item_data)

                    sort_by_type_0.append(sort_by_type_0_item)

                return sort_by_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[RunRunSortSpec] | None | Unset, data)

        sort_by = _parse_sort_by(d.pop("sort_by", UNSET))

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

        def _parse_trigger_filter(data: object) -> list[str] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                trigger_filter_type_0 = cast(list[str], data)

                return trigger_filter_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[str] | None | Unset, data)

        trigger_filter = _parse_trigger_filter(d.pop("trigger_filter", UNSET))

        workflow_id = d.pop("workflow_id", UNSET)

        run_run_list_request = cls(
            limit=limit,
            offset=offset,
            schema=schema,
            search=search,
            sort_by=sort_by,
            status_filter=status_filter,
            trigger_filter=trigger_filter,
            workflow_id=workflow_id,
        )

        return run_run_list_request
