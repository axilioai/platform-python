from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.phone_active_session import PhoneActiveSession


T = TypeVar("T", bound="PhoneActiveSessionsResponse")


@_attrs_define
class PhoneActiveSessionsResponse:
    """
    Attributes:
        sessions (list[PhoneActiveSession] | None):
        total (int):
        schema (str | Unset): A URL to the JSON Schema for this object.
    """

    sessions: list[PhoneActiveSession] | None
    total: int
    schema: str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
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
                "sessions": sessions,
                "total": total,
            }
        )
        if schema is not UNSET:
            field_dict["$schema"] = schema

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.phone_active_session import PhoneActiveSession

        d = dict(src_dict)

        def _parse_sessions(data: object) -> list[PhoneActiveSession] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                sessions_type_0 = []
                _sessions_type_0 = data
                for sessions_type_0_item_data in _sessions_type_0:
                    sessions_type_0_item = PhoneActiveSession.from_dict(sessions_type_0_item_data)

                    sessions_type_0.append(sessions_type_0_item)

                return sessions_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[PhoneActiveSession] | None, data)

        sessions = _parse_sessions(d.pop("sessions"))

        total = d.pop("total")

        schema = d.pop("$schema", UNSET)

        phone_active_sessions_response = cls(
            sessions=sessions,
            total=total,
            schema=schema,
        )

        return phone_active_sessions_response
