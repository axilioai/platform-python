from __future__ import annotations

import pytest

from scripts.patch_generated_frames import UNPATCHED_UNION, patch_source


def test_generated_frame_patch_is_idempotent() -> None:
    source = "# generated header\n" + UNPATCHED_UNION
    patched, changed = patch_source(source)
    assert changed
    assert "class RunSessionFramesResponseFramesItem_Unknown" in patched

    patched_again, changed_again = patch_source(patched)
    assert not changed_again
    assert patched_again == patched


def test_generated_frame_patch_fails_closed_on_generator_drift() -> None:
    with pytest.raises(ValueError, match="generator output"):
        patch_source("RunSessionFramesResponseFramesItem = object\n")
