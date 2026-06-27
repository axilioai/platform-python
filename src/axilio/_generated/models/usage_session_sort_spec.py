from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="UsageSessionSortSpec")


@_attrs_define
class UsageSessionSortSpec:
    """
    Attributes:
        field (str):
        order (str):
    """

    field: str
    order: str

    def to_dict(self) -> dict[str, Any]:
        field = self.field

        order = self.order

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "field": field,
                "order": order,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        field = d.pop("field")

        order = d.pop("order")

        usage_session_sort_spec = cls(
            field=field,
            order=order,
        )

        return usage_session_sort_spec
