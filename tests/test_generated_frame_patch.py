from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from types import ModuleType

import pytest


def _load_patch_script() -> ModuleType:
    path = Path(__file__).parents[1] / "scripts" / "patch_generated_frames.py"
    spec = importlib.util.spec_from_file_location("patch_generated_frames", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


_PATCH_SCRIPT = _load_patch_script()
UNPATCHED_UNION = _PATCH_SCRIPT.UNPATCHED_UNION
patch_source = _PATCH_SCRIPT.patch_source


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
