from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="ApikeyAPIKeyListItem")


@_attrs_define
class ApikeyAPIKeyListItem:
    """
    Attributes:
        created_at (datetime.datetime):
        id (str):
        key_preview (str):
        name (str):
        created_by (str | Unset):
        created_by_id (str | Unset):
        last_used_at (datetime.datetime | Unset):
    """

    created_at: datetime.datetime
    id: str
    key_preview: str
    name: str
    created_by: str | Unset = UNSET
    created_by_id: str | Unset = UNSET
    last_used_at: datetime.datetime | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        created_at = self.created_at.isoformat()

        id = self.id

        key_preview = self.key_preview

        name = self.name

        created_by = self.created_by

        created_by_id = self.created_by_id

        last_used_at: str | Unset = UNSET
        if not isinstance(self.last_used_at, Unset):
            last_used_at = self.last_used_at.isoformat()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "created_at": created_at,
                "id": id,
                "key_preview": key_preview,
                "name": name,
            }
        )
        if created_by is not UNSET:
            field_dict["created_by"] = created_by
        if created_by_id is not UNSET:
            field_dict["created_by_id"] = created_by_id
        if last_used_at is not UNSET:
            field_dict["last_used_at"] = last_used_at

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        created_at = datetime.datetime.fromisoformat(d.pop("created_at"))

        id = d.pop("id")

        key_preview = d.pop("key_preview")

        name = d.pop("name")

        created_by = d.pop("created_by", UNSET)

        created_by_id = d.pop("created_by_id", UNSET)

        _last_used_at = d.pop("last_used_at", UNSET)
        last_used_at: datetime.datetime | Unset
        if isinstance(_last_used_at, Unset):
            last_used_at = UNSET
        else:
            last_used_at = datetime.datetime.fromisoformat(_last_used_at)

        apikey_api_key_list_item = cls(
            created_at=created_at,
            id=id,
            key_preview=key_preview,
            name=name,
            created_by=created_by,
            created_by_id=created_by_id,
            last_used_at=last_used_at,
        )

        return apikey_api_key_list_item
