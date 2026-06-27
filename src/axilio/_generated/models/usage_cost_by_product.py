from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="UsageCostByProduct")


@_attrs_define
class UsageCostByProduct:
    """
    Attributes:
        inference (float):
        other (float):
        sessions (float):
    """

    inference: float
    other: float
    sessions: float

    def to_dict(self) -> dict[str, Any]:
        inference = self.inference

        other = self.other

        sessions = self.sessions

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "inference": inference,
                "other": other,
                "sessions": sessions,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        inference = d.pop("inference")

        other = d.pop("other")

        sessions = d.pop("sessions")

        usage_cost_by_product = cls(
            inference=inference,
            other=other,
            sessions=sessions,
        )

        return usage_cost_by_product
