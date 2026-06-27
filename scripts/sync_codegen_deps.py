"""Sync openapi-python-client's runtime deps into our pyproject.toml.

regen.sh builds the generator's output into a wheel (using the same
build backend the generator's pyproject declares — poetry-core, today)
and hands the resulting .whl to this script. We read the wheel's
``.dist-info/METADATA`` file's ``Requires-Dist:`` headers and write
them into a marker-fenced region of our parent pyproject's
``dependencies`` array.

Why "build a wheel and read METADATA" instead of parsing the
generator's pyproject directly: the build backend (Poetry, currently)
already does the canonical Poetry → PEP 508 translation when it
emits the wheel — that's the exact translation pip itself sees at
install time. Reading METADATA piggybacks on that, so we never have
to hand-roll a Poetry version-spec parser ourselves. The earlier
iteration of this script did, with edge-case doctests for caret
semver math; this version replaces ~80 lines of homegrown parsing
with ``email.parser.Parser`` on a stdlib zipfile entry.

It also makes the script future-proof against generator schema
changes: if openapi-python-client switches from Poetry to Hatch or
setuptools tomorrow, the wheel still has standard PEP 508
``Requires-Dist`` headers and this code keeps working.

The class of bug this prevents: generator adds a new transitive dep
(say, pydantic-core in some future minor version) — the new code
lands in ``src/axilio/_generated/`` on regen, but our pyproject's
``dependencies`` array still ships the old list. ``pip install
axilio`` succeeds, ``from axilio import Client`` fails with
``ModuleNotFoundError``. This guards the regression where ``axilio
0.1.1`` shipped without ``attrs`` / ``python-dateutil`` declared.

Usage::

    python scripts/sync_codegen_deps.py \\
        --wheel path/to/axilio_api_client-X.Y.Z-py3-none-any.whl \\
        --target path/to/our/pyproject.toml
"""

from __future__ import annotations

import argparse
import sys
import zipfile
from email.parser import BytesParser
from pathlib import Path

BEGIN_MARKER = "# ===== BEGIN GENERATED — DO NOT EDIT (regen.sh manages this) ====="
END_MARKER = "# ===== END GENERATED ====="


def read_requires_dist(wheel_path: Path) -> list[str]:
    """Return the wheel's ``Requires-Dist`` headers as canonical PEP 508 strings.

    Wheel ``METADATA`` is RFC 822-format text; we read it via stdlib
    ``email.parser`` directly from the zipped wheel without unpacking.
    Some build backends still emit the legacy parenthesised form
    (``name (>=1,<2)``); :func:`_canonicalize_pep508` flattens that to
    the modern bare form (``name>=1,<2``) so the rendered pyproject
    looks uniform regardless of which backend produced the input.
    """
    with zipfile.ZipFile(wheel_path) as zf:
        try:
            metadata_name = next(n for n in zf.namelist() if n.endswith(".dist-info/METADATA"))
        except StopIteration:
            raise SystemExit(
                f"{wheel_path}: no .dist-info/METADATA in the wheel — "
                f"is this actually a valid wheel?"
            ) from None
        with zf.open(metadata_name) as f:
            metadata = BytesParser().parse(f, headersonly=False)
    return [_canonicalize_pep508(d) for d in metadata.get_all("Requires-Dist") or []]


def _canonicalize_pep508(dep: str) -> str:
    """Strip the legacy parens-around-specifier form and surplus whitespace.

    >>> _canonicalize_pep508("httpx (>=0.23.0,<0.29.0)")
    'httpx>=0.23.0,<0.29.0'
    >>> _canonicalize_pep508("attrs >= 22.2.0")
    'attrs>=22.2.0'
    >>> _canonicalize_pep508("python-dateutil")
    'python-dateutil'
    """
    dep = dep.strip()
    if "(" in dep and dep.endswith(")"):
        name, _, rest = dep.partition("(")
        return f"{name.strip()}{rest[:-1].strip()}".replace(" ", "")
    return dep.replace(" ", "")


def rewrite_target(target_path: Path, deps: list[str]) -> bool:
    """Replace the marker-fenced region of ``target_path``'s ``dependencies``
    array with ``deps``. Returns True if the file changed, False if the
    rendered output already matches what's on disk."""
    text = target_path.read_text()
    try:
        begin = text.index(BEGIN_MARKER)
        end = text.index(END_MARKER, begin)
    except ValueError as exc:
        raise SystemExit(
            f"{target_path} is missing the regen marker block. Expected:\n"
            f"  {BEGIN_MARKER}\n"
            f"  {END_MARKER}\n"
            f"Add them inside the project.dependencies = [...] array; this "
            f"script rewrites everything between them on each run."
        ) from exc

    # Use the BEGIN marker line's leading whitespace as the indent for
    # each generated entry so they sit at the same depth as the
    # hand-written deps above the marker.
    line_start = text.rfind("\n", 0, begin) + 1
    indent = text[line_start:begin]

    rendered = BEGIN_MARKER + "\n"
    for dep in deps:
        rendered += f'{indent}"{dep}",\n'
    rendered += indent + END_MARKER

    new_text = text[:begin] + rendered + text[end + len(END_MARKER) :]
    if new_text == text:
        return False
    target_path.write_text(new_text)
    return True


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0] if __doc__ else "")
    parser.add_argument(
        "--wheel",
        required=True,
        type=Path,
        help="Path to a wheel built from the openapi-python-client output.",
    )
    parser.add_argument(
        "--target",
        required=True,
        type=Path,
        help="Path to our parent pyproject.toml that should receive the deps.",
    )
    args = parser.parse_args(argv)

    if not args.wheel.is_file():
        raise SystemExit(f"wheel not found: {args.wheel}")
    if not args.target.is_file():
        raise SystemExit(f"target pyproject not found: {args.target}")

    deps = read_requires_dist(args.wheel)
    if not deps:
        raise SystemExit(
            f"{args.wheel} declares no Requires-Dist headers — refusing to "
            f"wipe the marker block to an empty list (almost certainly a "
            f"generator or build-backend regression)."
        )

    if rewrite_target(args.target, deps):
        print(f"synced {len(deps)} runtime deps from generator into {args.target}")
    else:
        print(f"runtime deps already in sync with generator ({len(deps)} pkgs)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
