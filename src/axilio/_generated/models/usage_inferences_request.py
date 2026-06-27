from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.usage_inference_sort_spec import UsageInferenceSortSpec


T = TypeVar("T", bound="UsageInferencesRequest")


@_attrs_define
class UsageInferencesRequest:
    """
    Attributes:
        end_date (datetime.datetime):
        start_date (datetime.datetime):
        schema (str | Unset): A URL to the JSON Schema for this object.
        endpoint_filter (list[str] | None | Unset):
        limit (int | Unset):
        model (str | Unset):
        offset (int | Unset):
        search (str | Unset):
        session_id (str | Unset):
        sort_by (list[UsageInferenceSortSpec] | None | Unset):
    """

    end_date: datetime.datetime
    start_date: datetime.datetime
    schema: str | Unset = UNSET
    endpoint_filter: list[str] | None | Unset = UNSET
    limit: int | Unset = UNSET
    model: str | Unset = UNSET
    offset: int | Unset = UNSET
    search: str | Unset = UNSET
    session_id: str | Unset = UNSET
    sort_by: list[UsageInferenceSortSpec] | None | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        end_date = self.end_date.isoformat()

        start_date = self.start_date.isoformat()

        schema = self.schema

        endpoint_filter: list[str] | None | Unset
        if isinstance(self.endpoint_filter, Unset):
            endpoint_filter = UNSET
        elif isinstance(self.endpoint_filter, list):
            endpoint_filter = self.endpoint_filter

        else:
            endpoint_filter = self.endpoint_filter

        limit = self.limit

        model = self.model

        offset = self.offset

        search = self.search

        session_id = self.session_id

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

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "end_date": end_date,
                "start_date": start_date,
            }
        )
        if schema is not UNSET:
            field_dict["$schema"] = schema
        if endpoint_filter is not UNSET:
            field_dict["endpoint_filter"] = endpoint_filter
        if limit is not UNSET:
            field_dict["limit"] = limit
        if model is not UNSET:
            field_dict["model"] = model
        if offset is not UNSET:
            field_dict["offset"] = offset
        if search is not UNSET:
            field_dict["search"] = search
        if session_id is not UNSET:
            field_dict["session_id"] = session_id
        if sort_by is not UNSET:
            field_dict["sort_by"] = sort_by

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.usage_inference_sort_spec import UsageInferenceSortSpec

        d = dict(src_dict)
        end_date = datetime.datetime.fromisoformat(d.pop("end_date"))

        start_date = datetime.datetime.fromisoformat(d.pop("start_date"))

        schema = d.pop("$schema", UNSET)

        def _parse_endpoint_filter(data: object) -> list[str] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                endpoint_filter_type_0 = cast(list[str], data)

                return endpoint_filter_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[str] | None | Unset, data)

        endpoint_filter = _parse_endpoint_filter(d.pop("endpoint_filter", UNSET))

        limit = d.pop("limit", UNSET)

        model = d.pop("model", UNSET)

        offset = d.pop("offset", UNSET)

        search = d.pop("search", UNSET)

        session_id = d.pop("session_id", UNSET)

        def _parse_sort_by(data: object) -> list[UsageInferenceSortSpec] | None | Unset:
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
                    sort_by_type_0_item = UsageInferenceSortSpec.from_dict(sort_by_type_0_item_data)

                    sort_by_type_0.append(sort_by_type_0_item)

                return sort_by_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[UsageInferenceSortSpec] | None | Unset, data)

        sort_by = _parse_sort_by(d.pop("sort_by", UNSET))

        usage_inferences_request = cls(
            end_date=end_date,
            start_date=start_date,
            schema=schema,
            endpoint_filter=endpoint_filter,
            limit=limit,
            model=model,
            offset=offset,
            search=search,
            session_id=session_id,
            sort_by=sort_by,
        )

        return usage_inferences_request
