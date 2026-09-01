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
PATCHED_LOG_KIND = _PATCH_SCRIPT.PATCHED_LOG_KIND
PATCHED_SPAN_KIND = _PATCH_SCRIPT.PATCHED_SPAN_KIND
PATCHED_UNION = _PATCH_SCRIPT.PATCHED_UNION
TOP_LEVEL_EXPORT_INSERTIONS = _PATCH_SCRIPT.TOP_LEVEL_EXPORT_INSERTIONS
TYPE_EXPORT_INSERTIONS = _PATCH_SCRIPT.TYPE_EXPORT_INSERTIONS
UNPATCHED_LOG_KIND = _PATCH_SCRIPT.UNPATCHED_LOG_KIND
UNPATCHED_SPAN_KIND = _PATCH_SCRIPT.UNPATCHED_SPAN_KIND
UNPATCHED_UNION = _PATCH_SCRIPT.UNPATCHED_UNION
patch_exports = _PATCH_SCRIPT.patch_exports
patch_source = _PATCH_SCRIPT.patch_source


def test_generated_frame_patch_is_idempotent() -> None:
    source = "# generated header\n" + UNPATCHED_LOG_KIND + UNPATCHED_SPAN_KIND + UNPATCHED_UNION
    patched, changed = patch_source(source)
    assert changed
    assert PATCHED_UNION in patched
    assert PATCHED_LOG_KIND in patched
    assert PATCHED_SPAN_KIND in patched

    patched_again, changed_again = patch_source(patched)
    assert not changed_again
    assert patched_again == patched


def test_generated_frame_patch_fails_closed_on_generator_drift() -> None:
    with pytest.raises(ValueError, match="generator output"):
        patch_source("RunSessionFramesResponseFramesItem = object\n")


def test_generated_frame_patch_rejects_truncated_previous_patch() -> None:
    source = (
        UNPATCHED_LOG_KIND
        + UNPATCHED_SPAN_KIND
        + "class RunSessionFramesResponseFramesItem_Unknown:\n    pass\n"
    )
    with pytest.raises(ValueError, match="generator output"):
        patch_source(source)


def test_generated_frame_patch_upgrades_legacy_complete_union() -> None:
    source = UNPATCHED_LOG_KIND + UNPATCHED_SPAN_KIND + PATCHED_UNION
    patched, changed = patch_source(source)
    assert changed
    assert PATCHED_LOG_KIND in patched
    assert PATCHED_SPAN_KIND in patched
    assert UNPATCHED_LOG_KIND not in patched
    assert UNPATCHED_SPAN_KIND not in patched


@pytest.mark.parametrize(
    ("insertions", "label"),
    [(TYPE_EXPORT_INSERTIONS, "types"), (TOP_LEVEL_EXPORT_INSERTIONS, "top-level")],
)
def test_export_patch_is_idempotent_and_fails_closed_on_partial_state(
    insertions: tuple[tuple[str, str], ...], label: str
) -> None:
    source = "".join(anchor for anchor, _ in insertions)
    patched, changed = patch_exports(source, insertions, label)
    assert changed
    assert all(addition in patched for _, addition in insertions)

    patched_again, changed_again = patch_exports(patched, insertions, label)
    assert not changed_again
    assert patched_again == patched

    partial = patched.replace(insertions[0][1], "")
    with pytest.raises(ValueError, match="partially patched"):
        patch_exports(partial, insertions, label)
