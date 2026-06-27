from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="InferenceMetadata")


@_attrs_define
class InferenceMetadata:
    """
    Attributes:
        icon_detections_after_nms (int): Number of icon detections after NMS filtering
        icon_detections_before_nms (int): Number of icon detections before NMS filtering
        image_height (int): Input image height
        image_width (int): Input image width
        inference_time_ms (float): Total inference time in milliseconds
    """

    icon_detections_after_nms: int
    icon_detections_before_nms: int
    image_height: int
    image_width: int
    inference_time_ms: float
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        icon_detections_after_nms = self.icon_detections_after_nms

        icon_detections_before_nms = self.icon_detections_before_nms

        image_height = self.image_height

        image_width = self.image_width

        inference_time_ms = self.inference_time_ms

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "icon_detections_after_nms": icon_detections_after_nms,
                "icon_detections_before_nms": icon_detections_before_nms,
                "image_height": image_height,
                "image_width": image_width,
                "inference_time_ms": inference_time_ms,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        icon_detections_after_nms = d.pop("icon_detections_after_nms")

        icon_detections_before_nms = d.pop("icon_detections_before_nms")

        image_height = d.pop("image_height")

        image_width = d.pop("image_width")

        inference_time_ms = d.pop("inference_time_ms")

        inference_metadata = cls(
            icon_detections_after_nms=icon_detections_after_nms,
            icon_detections_before_nms=icon_detections_before_nms,
            image_height=image_height,
            image_width=image_width,
            inference_time_ms=inference_time_ms,
        )

        inference_metadata.additional_properties = d
        return inference_metadata

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
