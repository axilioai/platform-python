"""Make Fern's generated telemetry-frame union forward compatible.

Fern 5.15.0 emits the frame item as a strict Pydantic discriminated union, so
one future ``kind`` rejects the complete REST response before the hand-written
Telemetry helper can preserve it.  Run this immediately after every backend
regen.  It owns only the union seam: the known span/log fields remain entirely
generator-owned.

The transformation is intentionally exact and fail-closed.  A generator shape
change must break regen and force a review instead of silently removing the
tolerant-reader contract (AXI-1982).
"""

from __future__ import annotations

import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
FRAME_ITEM = REPO / "src" / "axilio" / "types" / "run_session_frames_response_frames_item.py"

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


def patch_source(source: str) -> tuple[str, bool]:
    if "class RunSessionFramesResponseFramesItem_Unknown" in source:
        return source, False
    if source.count(UNPATCHED_UNION) != 1:
        raise ValueError(
            "generated frame union no longer matches Fern 5.15.0; "
            "review the generator output and update this patch deliberately"
        )
    return source.replace(UNPATCHED_UNION, PATCHED_UNION), True


def main() -> int:
    try:
        source = FRAME_ITEM.read_text()
        patched, changed = patch_source(source)
    except (OSError, ValueError) as exc:
        print(f"patch_generated_frames: {exc}", file=sys.stderr)
        return 1
    if changed:
        FRAME_ITEM.write_text(patched)
        print("patched generated telemetry-frame union")
    else:
        print("generated telemetry-frame union already patched")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
