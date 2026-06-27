"""ArgusResource — client.argus.*

Direct access to Argus, Axilio's vision-inference service: object
detection (YOLO), OCR (free / premium engines), and a VLM-backed element
locator. This is the *direct* public surface — distinct from the
in-sandbox device-control path, where the on-device agent calls Argus
on the SDK's behalf. All read-style inference; available in both local
and sandbox modes.

Method bodies are stubs pending the SDK's generated-client wiring (the
whole resource layer is `codegen pending` today); the generated typed
client already exists under `axilio._generated_argus`.
"""

from __future__ import annotations

from .._resource import _Resource
from .types import InferenceResult, InferenceType, LocateResult, OcrEngine, TextElement


class ArgusResource(_Resource):
    """client.argus — vision inference (detect / OCR / locate)."""

    def infer(
        self,
        image: bytes,
        *,
        inference_type: InferenceType = "combined",
        confidence_threshold: float = 0.25,
        nms_iou_threshold: float = 0.45,
        ocr_engine: OcrEngine = "free",
    ) -> InferenceResult:
        """Run object detection and/or OCR over `image`.

        Args:
            image: Raw image bytes (PNG/JPEG).
            inference_type: Which passes to run — ``"yolo"`` (icons only),
                ``"ocr"`` (text only), or ``"combined"`` (both).
            confidence_threshold: Minimum detection confidence [0, 1].
            nms_iou_threshold: Non-max-suppression IoU threshold [0, 1].
            ocr_engine: ``"free"`` (RapidOCR) or ``"premium"`` (higher
                accuracy, billed per page). The provider name never leaks.
        """
        raise NotImplementedError("ArgusResource.infer — codegen pending")

    def locate(
        self,
        image: bytes,
        *,
        query: str,
        texts: list[TextElement] | None = None,
    ) -> LocateResult:
        """Find the UI element described by `query` in `image` (VLM-backed).

        Args:
            image: Raw image bytes (PNG/JPEG).
            query: Natural-language description of the element to find,
                e.g. ``"the login button"``.
            texts: Optional pre-computed OCR elements to ground the answer
                to a known on-screen region; when omitted the model returns
                a free-form pixel box.
        """
        raise NotImplementedError("ArgusResource.locate — codegen pending")
