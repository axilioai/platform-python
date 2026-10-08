"""Point the argus client's aiohttp install hint at the real extra after a regen.

Fern words the hint from each generator's ``package_name``. The argus client is
generated with ``package_name: "axilio.argus"`` (its import path), so its
``DefaultAioHttpClient`` tells users to ``pip install axilio.argus[aiohttp]``, a
distribution that does not exist. The extra lives on ``axilio`` (AXI-2227).

Run by the regen workflow after every generation. Idempotent, and exits non-zero
when neither form of the hint is found, so a generator wording change surfaces
as a failed regen instead of a silently wrong hint.
"""

from __future__ import annotations

import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
TARGET = REPO / "src" / "axilio" / "argus" / "_default_clients.py"
WRONG = "pip install axilio.argus[aiohttp]"
RIGHT = "pip install axilio[aiohttp]"


def main() -> int:
    src = TARGET.read_text(encoding="utf-8")
    if WRONG in src:
        TARGET.write_text(src.replace(WRONG, RIGHT), encoding="utf-8", newline="\n")
        print("fixed the argus aiohttp install hint")
        return 0
    if RIGHT in src:
        print("argus aiohttp install hint already correct")
        return 0
    print(
        f"fix_generated_install_hints: {TARGET.relative_to(REPO)}: neither {WRONG!r} nor "
        f"{RIGHT!r} found - the generator's wording changed; update this fix",
        file=sys.stderr,
    )
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
