from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.inference_type import InferenceType
from ..types import UNSET, Unset

T = TypeVar("T", bound="InferenceRequest")


@_attrs_define
class InferenceRequest:
    """
    Attributes:
        image (str): Base64 encoded image data
        confidence_threshold (float | Unset): Minimum confidence threshold for detections and OCR results Default: 0.25.
        inference_type (InferenceType | Unset):
        nms_iou_threshold (float | Unset): IoU threshold for Non-Maximum Suppression (NMS) Default: 0.45.
        ocr_engine (str | Unset): OCR engine to use: 'free' or 'premium' Default: 'free'.
    """

    image: str
    confidence_threshold: float | Unset = 0.25
    inference_type: InferenceType | Unset = UNSET
    nms_iou_threshold: float | Unset = 0.45
    ocr_engine: str | Unset = "free"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        image = self.image

        confidence_threshold = self.confidence_threshold

        inference_type: str | Unset = UNSET
        if not isinstance(self.inference_type, Unset):
            inference_type = self.inference_type.value

        nms_iou_threshold = self.nms_iou_threshold

        ocr_engine = self.ocr_engine

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "image": image,
            }
        )
        if confidence_threshold is not UNSET:
            field_dict["confidence_threshold"] = confidence_threshold
        if inference_type is not UNSET:
            field_dict["inference_type"] = inference_type
        if nms_iou_threshold is not UNSET:
            field_dict["nms_iou_threshold"] = nms_iou_threshold
        if ocr_engine is not UNSET:
            field_dict["ocr_engine"] = ocr_engine

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        image = d.pop("image")

        confidence_threshold = d.pop("confidence_threshold", UNSET)

        _inference_type = d.pop("inference_type", UNSET)
        inference_type: InferenceType | Unset
        if isinstance(_inference_type, Unset):
            inference_type = UNSET
        else:
            inference_type = InferenceType(_inference_type)

        nms_iou_threshold = d.pop("nms_iou_threshold", UNSET)

        ocr_engine = d.pop("ocr_engine", UNSET)

        inference_request = cls(
            image=image,
            confidence_threshold=confidence_threshold,
            inference_type=inference_type,
            nms_iou_threshold=nms_iou_threshold,
            ocr_engine=ocr_engine,
        )

        inference_request.additional_properties = d
        return inference_request

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
