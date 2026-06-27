from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.content_bounds import ContentBounds


T = TypeVar("T", bound="HashResult")


@_attrs_define
class HashResult:
    """
    Attributes:
        ahash (str): Average hash of the content area
        dhash (str): Difference hash of the content area
        phash (str): Perceptual hash of the content area
        content_bounds (ContentBounds | None | Unset): Content area bounds used for hashing
        histogram (list[list[int]] | None | Unset): RGB histogram (3 channels, 32 bins each)
    """

    ahash: str
    dhash: str
    phash: str
    content_bounds: ContentBounds | None | Unset = UNSET
    histogram: list[list[int]] | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.content_bounds import ContentBounds

        ahash = self.ahash

        dhash = self.dhash

        phash = self.phash

        content_bounds: dict[str, Any] | None | Unset
        if isinstance(self.content_bounds, Unset):
            content_bounds = UNSET
        elif isinstance(self.content_bounds, ContentBounds):
            content_bounds = self.content_bounds.to_dict()
        else:
            content_bounds = self.content_bounds

        histogram: list[list[int]] | None | Unset
        if isinstance(self.histogram, Unset):
            histogram = UNSET
        elif isinstance(self.histogram, list):
            histogram = []
            for histogram_type_0_item_data in self.histogram:
                histogram_type_0_item = histogram_type_0_item_data

                histogram.append(histogram_type_0_item)

        else:
            histogram = self.histogram

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "ahash": ahash,
                "dhash": dhash,
                "phash": phash,
            }
        )
        if content_bounds is not UNSET:
            field_dict["content_bounds"] = content_bounds
        if histogram is not UNSET:
            field_dict["histogram"] = histogram

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.content_bounds import ContentBounds

        d = dict(src_dict)
        ahash = d.pop("ahash")

        dhash = d.pop("dhash")

        phash = d.pop("phash")

        def _parse_content_bounds(data: object) -> ContentBounds | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                content_bounds_type_0 = ContentBounds.from_dict(data)

                return content_bounds_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(ContentBounds | None | Unset, data)

        content_bounds = _parse_content_bounds(d.pop("content_bounds", UNSET))

        def _parse_histogram(data: object) -> list[list[int]] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                histogram_type_0 = []
                _histogram_type_0 = data
                for histogram_type_0_item_data in _histogram_type_0:
                    histogram_type_0_item = cast(list[int], histogram_type_0_item_data)

                    histogram_type_0.append(histogram_type_0_item)

                return histogram_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[list[int]] | None | Unset, data)

        histogram = _parse_histogram(d.pop("histogram", UNSET))

        hash_result = cls(
            ahash=ahash,
            dhash=dhash,
            phash=phash,
            content_bounds=content_bounds,
            histogram=histogram,
        )

        hash_result.additional_properties = d
        return hash_result

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
