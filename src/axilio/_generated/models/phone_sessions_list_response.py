from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.phone_session_list_item import PhoneSessionListItem


T = TypeVar("T", bound="PhoneSessionsListResponse")


@_attrs_define
class PhoneSessionsListResponse:
    """
    Attributes:
        limit (int):
        offset (int):
        sessions (list[PhoneSessionListItem] | None):
        total (int):
        schema (str | Unset): A URL to the JSON Schema for this object.
    """

    limit: int
    offset: int
    sessions: list[PhoneSessionListItem] | None
    total: int
    schema: str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        limit = self.limit

        offset = self.offset

        sessions: list[dict[str, Any]] | None
        if isinstance(self.sessions, list):
            sessions = []
            for sessions_type_0_item_data in self.sessions:
                sessions_type_0_item = sessions_type_0_item_data.to_dict()
                sessions.append(sessions_type_0_item)

        else:
            sessions = self.sessions

        total = self.total

        schema = self.schema

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "limit": limit,
                "offset": offset,
                "sessions": sessions,
                "total": total,
            }
        )
        if schema is not UNSET:
            field_dict["$schema"] = schema

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.phone_session_list_item import PhoneSessionListItem

        d = dict(src_dict)
        limit = d.pop("limit")

        offset = d.pop("offset")

        def _parse_sessions(data: object) -> list[PhoneSessionListItem] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                sessions_type_0 = []
                _sessions_type_0 = data
                for sessions_type_0_item_data in _sessions_type_0:
                    sessions_type_0_item = PhoneSessionListItem.from_dict(sessions_type_0_item_data)

                    sessions_type_0.append(sessions_type_0_item)

                return sessions_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[PhoneSessionListItem] | None, data)

        sessions = _parse_sessions(d.pop("sessions"))

        total = d.pop("total")

        schema = d.pop("$schema", UNSET)

        phone_sessions_list_response = cls(
            limit=limit,
            offset=offset,
            sessions=sessions,
            total=total,
            schema=schema,
        )

        return phone_sessions_list_response
