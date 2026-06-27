from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.apikey_api_key_list_item import ApikeyAPIKeyListItem


T = TypeVar("T", bound="ApikeyAPIKeyListResponse")


@_attrs_define
class ApikeyAPIKeyListResponse:
    """
    Attributes:
        api_keys (list[ApikeyAPIKeyListItem] | None):
        limit (int):
        offset (int):
        total (int):
        schema (str | Unset): A URL to the JSON Schema for this object.
    """

    api_keys: list[ApikeyAPIKeyListItem] | None
    limit: int
    offset: int
    total: int
    schema: str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        api_keys: list[dict[str, Any]] | None
        if isinstance(self.api_keys, list):
            api_keys = []
            for api_keys_type_0_item_data in self.api_keys:
                api_keys_type_0_item = api_keys_type_0_item_data.to_dict()
                api_keys.append(api_keys_type_0_item)

        else:
            api_keys = self.api_keys

        limit = self.limit

        offset = self.offset

        total = self.total

        schema = self.schema

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "api_keys": api_keys,
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
        from ..models.apikey_api_key_list_item import ApikeyAPIKeyListItem

        d = dict(src_dict)

        def _parse_api_keys(data: object) -> list[ApikeyAPIKeyListItem] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                api_keys_type_0 = []
                _api_keys_type_0 = data
                for api_keys_type_0_item_data in _api_keys_type_0:
                    api_keys_type_0_item = ApikeyAPIKeyListItem.from_dict(api_keys_type_0_item_data)

                    api_keys_type_0.append(api_keys_type_0_item)

                return api_keys_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[ApikeyAPIKeyListItem] | None, data)

        api_keys = _parse_api_keys(d.pop("api_keys"))

        limit = d.pop("limit")

        offset = d.pop("offset")

        total = d.pop("total")

        schema = d.pop("$schema", UNSET)

        apikey_api_key_list_response = cls(
            api_keys=api_keys,
            limit=limit,
            offset=offset,
            total=total,
            schema=schema,
        )

        return apikey_api_key_list_response
