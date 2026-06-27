from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="UsageInference")


@_attrs_define
class UsageInference:
    """
    Attributes:
        cost_microdollars (int):
        created_at (str):
        endpoint (str):
        inference_id (str):
        latency_ms (int):
        model (str):
        ocr_pages (int):
        api_key_id (str | Unset):
        ocr_engine (str | Unset):
        session_id (str | Unset):
        vlm_model (str | Unset):
    """

    cost_microdollars: int
    created_at: str
    endpoint: str
    inference_id: str
    latency_ms: int
    model: str
    ocr_pages: int
    api_key_id: str | Unset = UNSET
    ocr_engine: str | Unset = UNSET
    session_id: str | Unset = UNSET
    vlm_model: str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        cost_microdollars = self.cost_microdollars

        created_at = self.created_at

        endpoint = self.endpoint

        inference_id = self.inference_id

        latency_ms = self.latency_ms

        model = self.model

        ocr_pages = self.ocr_pages

        api_key_id = self.api_key_id

        ocr_engine = self.ocr_engine

        session_id = self.session_id

        vlm_model = self.vlm_model

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "cost_microdollars": cost_microdollars,
                "created_at": created_at,
                "endpoint": endpoint,
                "inference_id": inference_id,
                "latency_ms": latency_ms,
                "model": model,
                "ocr_pages": ocr_pages,
            }
        )
        if api_key_id is not UNSET:
            field_dict["api_key_id"] = api_key_id
        if ocr_engine is not UNSET:
            field_dict["ocr_engine"] = ocr_engine
        if session_id is not UNSET:
            field_dict["session_id"] = session_id
        if vlm_model is not UNSET:
            field_dict["vlm_model"] = vlm_model

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        cost_microdollars = d.pop("cost_microdollars")

        created_at = d.pop("created_at")

        endpoint = d.pop("endpoint")

        inference_id = d.pop("inference_id")

        latency_ms = d.pop("latency_ms")

        model = d.pop("model")

        ocr_pages = d.pop("ocr_pages")

        api_key_id = d.pop("api_key_id", UNSET)

        ocr_engine = d.pop("ocr_engine", UNSET)

        session_id = d.pop("session_id", UNSET)

        vlm_model = d.pop("vlm_model", UNSET)

        usage_inference = cls(
            cost_microdollars=cost_microdollars,
            created_at=created_at,
            endpoint=endpoint,
            inference_id=inference_id,
            latency_ms=latency_ms,
            model=model,
            ocr_pages=ocr_pages,
            api_key_id=api_key_id,
            ocr_engine=ocr_engine,
            session_id=session_id,
            vlm_model=vlm_model,
        )

        return usage_inference
