from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.bounding_box import BoundingBox


T = TypeVar("T", bound="OCRResult")


@_attrs_define
class OCRResult:
    """
    Attributes:
        bbox (BoundingBox):
        confidence (float): OCR confidence score
        text (str): Detected text content
    """

    bbox: BoundingBox
    confidence: float
    text: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        bbox = self.bbox.to_dict()

        confidence = self.confidence

        text = self.text

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "bbox": bbox,
                "confidence": confidence,
                "text": text,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.bounding_box import BoundingBox

        d = dict(src_dict)
        bbox = BoundingBox.from_dict(d.pop("bbox"))

        confidence = d.pop("confidence")

        text = d.pop("text")

        ocr_result = cls(
            bbox=bbox,
            confidence=confidence,
            text=text,
        )

        ocr_result.additional_properties = d
        return ocr_result

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
