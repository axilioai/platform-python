"""Argus — direct vision inference (object detection, OCR, element locate)."""

from __future__ import annotations

from .resource import ArgusResource
from .types import (
    BoundingBox,
    IconDetection,
    InferenceResult,
    InferenceType,
    LocateResult,
    OcrEngine,
    OcrResult,
    TextElement,
)

__all__ = [
    "ArgusResource",
    "BoundingBox",
    "IconDetection",
    "InferenceResult",
    "InferenceType",
    "LocateResult",
    "OcrEngine",
    "OcrResult",
    "TextElement",
]
