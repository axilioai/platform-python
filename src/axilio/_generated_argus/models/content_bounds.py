from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="ContentBounds")


@_attrs_define
class ContentBounds:
    """
    Attributes:
        bottom_y (int): Bottom Y coordinate of content area (above nav bar)
        top_y (int): Top Y coordinate of content area (below notification bar)
    """

    bottom_y: int
    top_y: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        bottom_y = self.bottom_y

        top_y = self.top_y

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "bottom_y": bottom_y,
                "top_y": top_y,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        bottom_y = d.pop("bottom_y")

        top_y = d.pop("top_y")

        content_bounds = cls(
            bottom_y=bottom_y,
            top_y=top_y,
        )

        content_bounds.additional_properties = d
        return content_bounds

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
