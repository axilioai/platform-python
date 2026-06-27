from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.apikey_api_key_sort_spec import ApikeyAPIKeySortSpec


T = TypeVar("T", bound="ApikeyAPIKeyListRequest")


@_attrs_define
class ApikeyAPIKeyListRequest:
    """
    Attributes:
        limit (int):
        offset (int):
        schema (str | Unset): A URL to the JSON Schema for this object.
        created_after (datetime.datetime | Unset):
        created_before (datetime.datetime | Unset):
        created_by (list[str] | None | Unset):
        search (str | Unset):
        sort_by (list[ApikeyAPIKeySortSpec] | None | Unset):
    """

    limit: int
    offset: int
    schema: str | Unset = UNSET
    created_after: datetime.datetime | Unset = UNSET
    created_before: datetime.datetime | Unset = UNSET
    created_by: list[str] | None | Unset = UNSET
    search: str | Unset = UNSET
    sort_by: list[ApikeyAPIKeySortSpec] | None | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        limit = self.limit

        offset = self.offset

        schema = self.schema

        created_after: str | Unset = UNSET
        if not isinstance(self.created_after, Unset):
            created_after = self.created_after.isoformat()

        created_before: str | Unset = UNSET
        if not isinstance(self.created_before, Unset):
            created_before = self.created_before.isoformat()

        created_by: list[str] | None | Unset
        if isinstance(self.created_by, Unset):
            created_by = UNSET
        elif isinstance(self.created_by, list):
            created_by = self.created_by

        else:
            created_by = self.created_by

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
        if created_by is not UNSET:
            field_dict["created_by"] = created_by
        if search is not UNSET:
            field_dict["search"] = search
        if sort_by is not UNSET:
            field_dict["sort_by"] = sort_by

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.apikey_api_key_sort_spec import ApikeyAPIKeySortSpec

        d = dict(src_dict)
        limit = d.pop("limit")

        offset = d.pop("offset")

        schema = d.pop("$schema", UNSET)

        _created_after = d.pop("created_after", UNSET)
        created_after: datetime.datetime | Unset
        if isinstance(_created_after, Unset):
            created_after = UNSET
        else:
            created_after = datetime.datetime.fromisoformat(_created_after)

        _created_before = d.pop("created_before", UNSET)
        created_before: datetime.datetime | Unset
        if isinstance(_created_before, Unset):
            created_before = UNSET
        else:
            created_before = datetime.datetime.fromisoformat(_created_before)

        def _parse_created_by(data: object) -> list[str] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                created_by_type_0 = cast(list[str], data)

                return created_by_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[str] | None | Unset, data)

        created_by = _parse_created_by(d.pop("created_by", UNSET))

        search = d.pop("search", UNSET)

        def _parse_sort_by(data: object) -> list[ApikeyAPIKeySortSpec] | None | Unset:
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
                    sort_by_type_0_item = ApikeyAPIKeySortSpec.from_dict(sort_by_type_0_item_data)

                    sort_by_type_0.append(sort_by_type_0_item)

                return sort_by_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[ApikeyAPIKeySortSpec] | None | Unset, data)

        sort_by = _parse_sort_by(d.pop("sort_by", UNSET))

        apikey_api_key_list_request = cls(
            limit=limit,
            offset=offset,
            schema=schema,
            created_after=created_after,
            created_before=created_before,
            created_by=created_by,
            search=search,
            sort_by=sort_by,
        )

        return apikey_api_key_list_request
