from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.locate_b_box import LocateBBox


T = TypeVar("T", bound="LocateResponse")


@_attrs_define
class LocateResponse:
    """Argus /inference/locate response.

    Exactly one of `matched_text_index` or `bbox` is populated when
    `found` is True. `matched_text_index` indicates the VLM grounded its
    answer to a specific OCR text element (pixel-accurate bbox available
    via the original `texts` list). `bbox` is a free-form VLM bbox.

        Attributes:
            confidence (float): Model self-reported confidence
            cost_microdollars (int): Provider-reported cost in microdollars
            found (bool): Whether the VLM located the target
            latency_ms (int): End-to-end VLM call latency
            model (str): Model identifier returned by the provider
            bbox (LocateBBox | None | Unset): Pixel-space bbox. None when matched_text_index is set or found=False.
            completion_tokens (int | Unset): Completion (output) tokens the model billed for this call Default: 0.
            matched_text_index (int | None | Unset): Index into the request `texts` list when the answer is OCR-grounded.
            prompt_tokens (int | Unset): Prompt (input) tokens the model billed for this call Default: 0.
    """

    confidence: float
    cost_microdollars: int
    found: bool
    latency_ms: int
    model: str
    bbox: LocateBBox | None | Unset = UNSET
    completion_tokens: int | Unset = 0
    matched_text_index: int | None | Unset = UNSET
    prompt_tokens: int | Unset = 0
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.locate_b_box import LocateBBox

        confidence = self.confidence

        cost_microdollars = self.cost_microdollars

        found = self.found

        latency_ms = self.latency_ms

        model = self.model

        bbox: dict[str, Any] | None | Unset
        if isinstance(self.bbox, Unset):
            bbox = UNSET
        elif isinstance(self.bbox, LocateBBox):
            bbox = self.bbox.to_dict()
        else:
            bbox = self.bbox

        completion_tokens = self.completion_tokens

        matched_text_index: int | None | Unset
        if isinstance(self.matched_text_index, Unset):
            matched_text_index = UNSET
        else:
            matched_text_index = self.matched_text_index

        prompt_tokens = self.prompt_tokens

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "confidence": confidence,
                "cost_microdollars": cost_microdollars,
                "found": found,
                "latency_ms": latency_ms,
                "model": model,
            }
        )
        if bbox is not UNSET:
            field_dict["bbox"] = bbox
        if completion_tokens is not UNSET:
            field_dict["completion_tokens"] = completion_tokens
        if matched_text_index is not UNSET:
            field_dict["matched_text_index"] = matched_text_index
        if prompt_tokens is not UNSET:
            field_dict["prompt_tokens"] = prompt_tokens

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.locate_b_box import LocateBBox

        d = dict(src_dict)
        confidence = d.pop("confidence")

        cost_microdollars = d.pop("cost_microdollars")

        found = d.pop("found")

        latency_ms = d.pop("latency_ms")

        model = d.pop("model")

        def _parse_bbox(data: object) -> LocateBBox | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                bbox_type_0 = LocateBBox.from_dict(data)

                return bbox_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(LocateBBox | None | Unset, data)

        bbox = _parse_bbox(d.pop("bbox", UNSET))

        completion_tokens = d.pop("completion_tokens", UNSET)

        def _parse_matched_text_index(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        matched_text_index = _parse_matched_text_index(d.pop("matched_text_index", UNSET))

        prompt_tokens = d.pop("prompt_tokens", UNSET)

        locate_response = cls(
            confidence=confidence,
            cost_microdollars=cost_microdollars,
            found=found,
            latency_ms=latency_ms,
            model=model,
            bbox=bbox,
            completion_tokens=completion_tokens,
            matched_text_index=matched_text_index,
            prompt_tokens=prompt_tokens,
        )

        locate_response.additional_properties = d
        return locate_response

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
