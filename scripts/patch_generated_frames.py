"""Make Fern's generated telemetry-frame union forward compatible.

Fern 5.15.0 emits the frame item as a strict Pydantic discriminated union, so
one future ``kind`` rejects the complete REST response before the hand-written
Telemetry helper can preserve it. Run this immediately after every backend
regen. It owns the discriminator seam and the generated public exports for the
fallback type; every other known span/log field remains generator-owned.

The transformation is intentionally exact and fail-closed.  A generator shape
change must break regen and force a review instead of silently removing the
tolerant-reader contract (AXI-1982).
"""

from __future__ import annotations

import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
FRAME_ITEM = REPO / "src" / "axilio" / "types" / "run_session_frames_response_frames_item.py"
TYPES_EXPORTS = REPO / "src" / "axilio" / "types" / "__init__.py"
TOP_LEVEL_EXPORTS = REPO / "src" / "axilio" / "__init__.py"

UNPATCHED_LOG_KIND = """    kind: typing.Literal["log"] = "log"
    attributes: typing.Optional[typing.Dict[str, typing.Any]] = None
"""
PATCHED_LOG_KIND = """    kind: typing.Literal["log"]
    attributes: typing.Optional[typing.Dict[str, typing.Any]] = None
"""
UNPATCHED_SPAN_KIND = """    kind: typing.Literal["span"] = "span"
    attributes: typing.Optional[typing.Dict[str, typing.Any]] = None
"""
PATCHED_SPAN_KIND = """    kind: typing.Literal["span"]
    attributes: typing.Optional[typing.Dict[str, typing.Any]] = None
"""

UNPATCHED_UNION = """RunSessionFramesResponseFramesItem = typing_extensions.Annotated[
    typing.Union[RunSessionFramesResponseFramesItem_Log, RunSessionFramesResponseFramesItem_Span],
    pydantic.Field(discriminator="kind"),
]
"""

PATCHED_UNION = '''class RunSessionFramesResponseFramesItem_Unknown(UniversalBaseModel):
    """A future frame kind this SDK does not yet model.

    Extra fields retain the complete wire object. ``raw`` returns that object
    in its original semantic JSON shape for generic rendering or logging.
    """

    kind: pydantic.StrictStr

    if IS_PYDANTIC_V2:

        @pydantic.field_validator("kind")
        @classmethod
        def validate_unknown_kind(cls, value: str) -> str:
            if not value or value in {"log", "span"}:
                raise ValueError("unknown frame kind must be non-empty and not a known kind")
            return value

        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(
            extra="allow", frozen=True
        )  # type: ignore # Pydantic v2
    else:

        @pydantic.validator("kind")
        def validate_unknown_kind(cls, value: str) -> str:
            if not value or value in {"log", "span"}:
                raise ValueError("unknown frame kind must be non-empty and not a known kind")
            return value

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow

    @property
    def raw(self) -> typing.Dict[str, typing.Any]:
        if IS_PYDANTIC_V2:
            return typing.cast(typing.Dict[str, typing.Any], self.model_dump(by_alias=True))
        return typing.cast(typing.Dict[str, typing.Any], self.dict(by_alias=True))


RunSessionFramesResponseFramesItem = typing.Union[
    RunSessionFramesResponseFramesItem_Log,
    RunSessionFramesResponseFramesItem_Span,
    RunSessionFramesResponseFramesItem_Unknown,
]
'''

TYPE_EXPORT_INSERTIONS = (
    (
        "        RunSessionFramesResponseFramesItem_Span,\n",
        "        RunSessionFramesResponseFramesItem_Unknown,\n",
    ),
    (
        '    "RunSessionFramesResponseFramesItem_Span": '
        '".run_session_frames_response_frames_item",\n',
        '    "RunSessionFramesResponseFramesItem_Unknown": '
        '".run_session_frames_response_frames_item",\n',
    ),
    (
        '    "RunSessionFramesResponseFramesItem_Span",\n',
        '    "RunSessionFramesResponseFramesItem_Unknown",\n',
    ),
)

TOP_LEVEL_EXPORT_INSERTIONS = (
    (
        "        RunSessionFramesResponseFramesItem_Span,\n",
        "        RunSessionFramesResponseFramesItem_Unknown,\n",
    ),
    (
        '    "RunSessionFramesResponseFramesItem_Span": ".types",\n',
        '    "RunSessionFramesResponseFramesItem_Unknown": ".types",\n',
    ),
    (
        '    "RunSessionFramesResponseFramesItem_Span",\n',
        '    "RunSessionFramesResponseFramesItem_Unknown",\n',
    ),
)


def patch_source(source: str) -> tuple[str, bool]:
    patched_union_count = source.count(PATCHED_UNION)
    unpatched_union_count = source.count(UNPATCHED_UNION)
    patched_kind_counts = (
        source.count(PATCHED_LOG_KIND),
        source.count(PATCHED_SPAN_KIND),
    )
    unpatched_kind_counts = (
        source.count(UNPATCHED_LOG_KIND),
        source.count(UNPATCHED_SPAN_KIND),
    )

    if (
        patched_union_count == 1
        and patched_kind_counts == (1, 1)
        and unpatched_kind_counts == (0, 0)
    ):
        return source, False
    if (
        patched_union_count == 1
        and patched_kind_counts == (0, 0)
        and unpatched_kind_counts == (1, 1)
    ):
        # Upgrade the first AXI-1982 patch, which added the fallback but left
        # Fern's discriminator defaults in place. Requiring the fields makes a
        # complete known-frame shape without ``kind`` fail under Pydantic 1/2.
        return (
            source.replace(UNPATCHED_LOG_KIND, PATCHED_LOG_KIND).replace(
                UNPATCHED_SPAN_KIND, PATCHED_SPAN_KIND
            ),
            True,
        )
    if (
        patched_union_count != 0
        or unpatched_union_count != 1
        or patched_kind_counts != (0, 0)
        or unpatched_kind_counts != (1, 1)
    ):
        raise ValueError(
            "generated frame union no longer matches Fern 5.15.0; "
            "review the generator output and update this patch deliberately"
        )
    return (
        source.replace(UNPATCHED_LOG_KIND, PATCHED_LOG_KIND)
        .replace(UNPATCHED_SPAN_KIND, PATCHED_SPAN_KIND)
        .replace(UNPATCHED_UNION, PATCHED_UNION),
        True,
    )


def patch_exports(
    source: str, insertions: tuple[tuple[str, str], ...], label: str
) -> tuple[str, bool]:
    states: list[bool] = []
    for anchor, addition in insertions:
        addition_count = source.count(addition)
        anchor_count = source.count(anchor)
        if addition_count not in {0, 1} or anchor_count != 1:
            raise ValueError(f"generated {label} exports changed shape; review the regen output")
        states.append(addition_count == 1)
    if all(states):
        return source, False
    if any(states):
        raise ValueError(f"generated {label} exports are only partially patched")
    for anchor, addition in insertions:
        source = source.replace(anchor, anchor + addition)
    return source, True


def main() -> int:
    try:
        targets = (
            (FRAME_ITEM, patch_source),
            (TYPES_EXPORTS, lambda source: patch_exports(source, TYPE_EXPORT_INSERTIONS, "types")),
            (
                TOP_LEVEL_EXPORTS,
                lambda source: patch_exports(source, TOP_LEVEL_EXPORT_INSERTIONS, "top-level"),
            ),
        )
        patches: list[tuple[pathlib.Path, str, bool]] = []
        for path, patcher in targets:
            patched, changed = patcher(path.read_text())
            patches.append((path, patched, changed))
    except (OSError, ValueError) as exc:
        print(f"patch_generated_frames: {exc}", file=sys.stderr)
        return 1
    changed_paths = []
    for path, patched, changed in patches:
        if changed:
            path.write_text(patched)
            changed_paths.append(path.relative_to(REPO).as_posix())
    if changed_paths:
        print(
            "patched generated telemetry-frame compatibility surface: " + ", ".join(changed_paths)
        )
    else:
        print("generated telemetry-frame union already patched")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
