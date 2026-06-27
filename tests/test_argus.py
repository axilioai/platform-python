"""Surface tests for the Argus resource. The methods are stubs
(`codegen pending`) like the rest of the SDK today, so these assert the
public shape — the resource hangs off the client, the typed signatures
exist, and the public dataclasses are importable + constructible — rather
than wire behavior. Functional tests land when the methods get wired up.
"""

from __future__ import annotations

import pytest

from axilio.argus import (
    ArgusResource,
    BoundingBox,
    InferenceResult,
    LocateResult,
    OcrResult,
    TextElement,
)
from axilio.platform import Client


def test_client_exposes_argus() -> None:
    client = Client(api_key="ax_test")
    try:
        assert isinstance(client.argus, ArgusResource)
    finally:
        client.close()


def test_infer_is_stubbed() -> None:
    client = Client(api_key="ax_test")
    try:
        with pytest.raises(NotImplementedError, match="codegen pending"):
            client.argus.infer(b"\x89PNG", inference_type="combined")
    finally:
        client.close()


def test_locate_is_stubbed() -> None:
    client = Client(api_key="ax_test")
    try:
        with pytest.raises(NotImplementedError, match="codegen pending"):
            client.argus.locate(b"\x89PNG", query="the login button")
    finally:
        client.close()


def test_public_types_construct() -> None:
    box = BoundingBox(x1=0.0, y1=0.0, x2=10.0, y2=20.0)
    ocr = OcrResult(text="Login", confidence=0.97, bbox=box)
    result = InferenceResult(
        ocr_results=[ocr],
        icons=[],
        inference_time_ms=12.5,
        image_width=1080,
        image_height=1920,
    )
    located = LocateResult(found=True, bbox=box, confidence=0.9, matched_text_index=0)
    elem = TextElement(text="Login", bbox=box)

    assert result.ocr_results[0].text == "Login"
    assert located.found is True
    assert elem.bbox is box
