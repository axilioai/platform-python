from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.detection import Detection
    from ..models.hash_result import HashResult
    from ..models.inference_metadata import InferenceMetadata
    from ..models.ocr_result import OCRResult


T = TypeVar("T", bound="InferenceData")


@_attrs_define
class InferenceData:
    """
    Attributes:
        metadata (InferenceMetadata):
        hash_result (HashResult | None | Unset): Image hash of content area
        icon_detections (list[Detection] | Unset): Icon detections (YOLO)
        ocr_results (list[OCRResult] | Unset): OCR text detections
    """

    metadata: InferenceMetadata
    hash_result: HashResult | None | Unset = UNSET
    icon_detections: list[Detection] | Unset = UNSET
    ocr_results: list[OCRResult] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.hash_result import HashResult

        metadata = self.metadata.to_dict()

        hash_result: dict[str, Any] | None | Unset
        if isinstance(self.hash_result, Unset):
            hash_result = UNSET
        elif isinstance(self.hash_result, HashResult):
            hash_result = self.hash_result.to_dict()
        else:
            hash_result = self.hash_result

        icon_detections: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.icon_detections, Unset):
            icon_detections = []
            for icon_detections_item_data in self.icon_detections:
                icon_detections_item = icon_detections_item_data.to_dict()
                icon_detections.append(icon_detections_item)

        ocr_results: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.ocr_results, Unset):
            ocr_results = []
            for ocr_results_item_data in self.ocr_results:
                ocr_results_item = ocr_results_item_data.to_dict()
                ocr_results.append(ocr_results_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "metadata": metadata,
            }
        )
        if hash_result is not UNSET:
            field_dict["hash_result"] = hash_result
        if icon_detections is not UNSET:
            field_dict["icon_detections"] = icon_detections
        if ocr_results is not UNSET:
            field_dict["ocr_results"] = ocr_results

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.detection import Detection
        from ..models.hash_result import HashResult
        from ..models.inference_metadata import InferenceMetadata
        from ..models.ocr_result import OCRResult

        d = dict(src_dict)
        metadata = InferenceMetadata.from_dict(d.pop("metadata"))

        def _parse_hash_result(data: object) -> HashResult | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                hash_result_type_0 = HashResult.from_dict(data)

                return hash_result_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(HashResult | None | Unset, data)

        hash_result = _parse_hash_result(d.pop("hash_result", UNSET))

        _icon_detections = d.pop("icon_detections", UNSET)
        icon_detections: list[Detection] | Unset = UNSET
        if _icon_detections is not UNSET:
            icon_detections = []
            for icon_detections_item_data in _icon_detections:
                icon_detections_item = Detection.from_dict(icon_detections_item_data)

                icon_detections.append(icon_detections_item)

        _ocr_results = d.pop("ocr_results", UNSET)
        ocr_results: list[OCRResult] | Unset = UNSET
        if _ocr_results is not UNSET:
            ocr_results = []
            for ocr_results_item_data in _ocr_results:
                ocr_results_item = OCRResult.from_dict(ocr_results_item_data)

                ocr_results.append(ocr_results_item)

        inference_data = cls(
            metadata=metadata,
            hash_result=hash_result,
            icon_detections=icon_detections,
            ocr_results=ocr_results,
        )

        inference_data.additional_properties = d
        return inference_data

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
