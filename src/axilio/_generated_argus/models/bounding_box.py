from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="BoundingBox")


@_attrs_define
class BoundingBox:
    """
    Attributes:
        x1 (float): Top-left x coordinate
        x2 (float): Bottom-right x coordinate
        y1 (float): Top-left y coordinate
        y2 (float): Bottom-right y coordinate
    """

    x1: float
    x2: float
    y1: float
    y2: float
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        x1 = self.x1

        x2 = self.x2

        y1 = self.y1

        y2 = self.y2

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "x1": x1,
                "x2": x2,
                "y1": y1,
                "y2": y2,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        x1 = d.pop("x1")

        x2 = d.pop("x2")

        y1 = d.pop("y1")

        y2 = d.pop("y2")

        bounding_box = cls(
            x1=x1,
            x2=x2,
            y1=y1,
            y2=y2,
        )

        bounding_box.additional_properties = d
        return bounding_box

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
