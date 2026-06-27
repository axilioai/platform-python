from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.workflow_workflow_sort_spec import WorkflowWorkflowSortSpec


T = TypeVar("T", bound="WorkflowWorkflowListRequest")


@_attrs_define
class WorkflowWorkflowListRequest:
    """
    Attributes:
        limit (int):
        offset (int):
        schema (str | Unset): A URL to the JSON Schema for this object.
        created_after (str | Unset):
        created_before (str | Unset):
        last_run_after (str | Unset):
        last_run_before (str | Unset):
        platform_filter (list[str] | None | Unset):
        search (str | Unset):
        sort_by (list[WorkflowWorkflowSortSpec] | None | Unset):
        status_filter (list[str] | None | Unset):
    """

    limit: int
    offset: int
    schema: str | Unset = UNSET
    created_after: str | Unset = UNSET
    created_before: str | Unset = UNSET
    last_run_after: str | Unset = UNSET
    last_run_before: str | Unset = UNSET
    platform_filter: list[str] | None | Unset = UNSET
    search: str | Unset = UNSET
    sort_by: list[WorkflowWorkflowSortSpec] | None | Unset = UNSET
    status_filter: list[str] | None | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        limit = self.limit

        offset = self.offset

        schema = self.schema

        created_after = self.created_after

        created_before = self.created_before

        last_run_after = self.last_run_after

        last_run_before = self.last_run_before

        platform_filter: list[str] | None | Unset
        if isinstance(self.platform_filter, Unset):
            platform_filter = UNSET
        elif isinstance(self.platform_filter, list):
            platform_filter = self.platform_filter

        else:
            platform_filter = self.platform_filter

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

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "limit": limit,
                "offset": offset,
            }
        )
        if schema is not UNSET:
            field_dict["$schema"] = schema
        if created_after is not UNSET:
            field_dict["created_after"] = created_after
        if created_before is not UNSET:
            field_dict["created_before"] = created_before
        if last_run_after is not UNSET:
            field_dict["last_run_after"] = last_run_after
        if last_run_before is not UNSET:
            field_dict["last_run_before"] = last_run_before
        if platform_filter is not UNSET:
            field_dict["platform_filter"] = platform_filter
        if search is not UNSET:
            field_dict["search"] = search
        if sort_by is not UNSET:
            field_dict["sort_by"] = sort_by
        if status_filter is not UNSET:
            field_dict["status_filter"] = status_filter

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.workflow_workflow_sort_spec import WorkflowWorkflowSortSpec

        d = dict(src_dict)
        limit = d.pop("limit")

        offset = d.pop("offset")

        schema = d.pop("$schema", UNSET)

        created_after = d.pop("created_after", UNSET)

        created_before = d.pop("created_before", UNSET)

        last_run_after = d.pop("last_run_after", UNSET)

        last_run_before = d.pop("last_run_before", UNSET)

        def _parse_platform_filter(data: object) -> list[str] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                platform_filter_type_0 = cast(list[str], data)

                return platform_filter_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[str] | None | Unset, data)

        platform_filter = _parse_platform_filter(d.pop("platform_filter", UNSET))

        search = d.pop("search", UNSET)

        def _parse_sort_by(data: object) -> list[WorkflowWorkflowSortSpec] | None | Unset:
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
                    sort_by_type_0_item = WorkflowWorkflowSortSpec.from_dict(sort_by_type_0_item_data)

                    sort_by_type_0.append(sort_by_type_0_item)

                return sort_by_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[WorkflowWorkflowSortSpec] | None | Unset, data)

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

        workflow_workflow_list_request = cls(
            limit=limit,
            offset=offset,
            schema=schema,
            created_after=created_after,
            created_before=created_before,
            last_run_after=last_run_after,
            last_run_before=last_run_before,
            platform_filter=platform_filter,
            search=search,
            sort_by=sort_by,
            status_filter=status_filter,
        )

        return workflow_workflow_list_request
