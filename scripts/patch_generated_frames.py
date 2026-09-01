"""Add the unknown-frame fallback that Fern 5.15.0 cannot generate.

The replacement is exact and idempotent so generator drift fails CI instead of
silently removing the AXI-1982 compatibility boundary.
"""

from __future__ import annotations

import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
FRAME_ITEM = REPO / "src" / "axilio" / "types" / "run_session_frames_response_frames_item.py"
TYPES_EXPORTS = REPO / "src" / "axilio" / "types" / "__init__.py"
TOP_LEVEL_EXPORTS = REPO / "src" / "axilio" / "__init__.py"

GENERATED_LOG_KIND = """    kind: typing.Literal["log"] = "log"
    attributes: typing.Optional[typing.Dict[str, typing.Any]] = None
"""
GENERATED_SPAN_KIND = """    kind: typing.Literal["span"] = "span"
    attributes: typing.Optional[typing.Dict[str, typing.Any]] = None
"""

UNPATCHED_UNION = """RunSessionFramesResponseFramesItem = typing_extensions.Annotated[
    typing.Union[RunSessionFramesResponseFramesItem_Log, RunSessionFramesResponseFramesItem_Span],
    pydantic.Field(discriminator="kind"),
]
"""

UNKNOWN_VARIANT = '''class RunSessionFramesResponseFramesItem_Unknown(UniversalBaseModel):
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
        return typing.cast(
            typing.Dict[str, typing.Any], UniversalBaseModel.dict(self, by_alias=True)
        )


'''

PATCHED_UNION = UNKNOWN_VARIANT + """RunSessionFramesResponseFramesItem = typing.Union[
    typing_extensions.Annotated[
        typing.Union[
            RunSessionFramesResponseFramesItem_Log,
            RunSessionFramesResponseFramesItem_Span,
        ],
        pydantic.Field(discriminator="kind"),
    ],
    RunSessionFramesResponseFramesItem_Unknown,
]
"""

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
    union_counts = source.count(UNPATCHED_UNION), source.count(PATCHED_UNION)
    kind_counts = source.count(GENERATED_LOG_KIND), source.count(GENERATED_SPAN_KIND)
    if union_counts == (0, 1) and kind_counts == (1, 1):
        return source, False
    if union_counts != (1, 0) or kind_counts != (1, 1):
        raise ValueError(
            "generated frame union no longer matches Fern 5.15.0; "
            "review the generator output and update this patch deliberately"
        )
    return source.replace(UNPATCHED_UNION, PATCHED_UNION), True


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
