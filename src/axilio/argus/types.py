"""Public types for Argus vision inference.

Hand-written, clean public shapes — deliberately decoupled from the
generated models under ``axilio._generated_argus`` so the customer-facing
surface stays stable even when codegen names churn. The resource wrapper
adapts generated models to / from these.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

InferenceType = Literal["yolo", "ocr", "combined"]
OcrEngine = Literal["free", "premium"]


@dataclass(frozen=True)
class BoundingBox:
    """Axis-aligned box in image-pixel coordinates (top-left origin)."""

    x1: float
    y1: float
    x2: float
    y2: float


@dataclass(frozen=True)
class OcrResult:
    """One recognised text region from the OCR pass."""

    text: str
    confidence: float
    bbox: BoundingBox


@dataclass(frozen=True)
class IconDetection:
    """One UI element detected by the object-detection (YOLO) pass."""

    bbox: BoundingBox
    confidence: float
    class_id: int
    class_name: str


@dataclass(frozen=True)
class InferenceResult:
    """Result of ``client.argus.infer`` — the OCR + object-detection
    passes over one image. ``ocr_results`` / ``icons`` are empty when the
    requested ``inference_type`` skipped that pass."""

    ocr_results: list[OcrResult]
    icons: list[IconDetection]
    inference_time_ms: float
    image_width: int
    image_height: int


@dataclass(frozen=True)
class TextElement:
    """A pre-computed OCR element fed into ``locate`` to ground the VLM's
    answer to a known on-screen region. ``bbox`` is normalised [0, 1]."""

    text: str
    bbox: BoundingBox


@dataclass(frozen=True)
class LocateResult:
    """Result of ``client.argus.locate`` — the VLM's attempt to find the
    element described by ``query``.

    ``found`` is False when the element isn't on screen (``bbox`` is then
    None). When found, ``bbox`` is in image-pixel coordinates and
    ``matched_text_index`` points into the ``texts`` passed to ``locate``
    if the answer was grounded to one of them (else None)."""

    found: bool
    bbox: BoundingBox | None
    confidence: float
    matched_text_index: int | None
