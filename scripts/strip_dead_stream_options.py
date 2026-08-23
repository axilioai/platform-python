"""Strip Fern's generated SSE stream-reconnect surface after a regen.

Nothing in this SDK reads ``stream_reconnection_enabled`` /
``max_stream_reconnection_attempts`` (client kwargs, wrapper state, or the
``RequestOptions`` entries): no generated endpoint streams, so the options
advertise transparent Last-Event-ID reconnection that silently does
nothing. The real reconnect contract lives in the hand-written DCP
transport (axilio.drivers.mobile). Deleting the dead surface keeps that
the only reconnect story advertised.

Run by the regen workflow after every generation. Exits non-zero when a
pattern no longer matches, so a generator-shape change surfaces as a
failed regen instead of silently resurrecting the dead surface.
"""

from __future__ import annotations

import pathlib
import re
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
SRC = REPO / "src" / "axilio"

_DOCSTRING = (
    r"\n    (?:stream_reconnection_enabled|max_stream_reconnection_attempts) :"
    r" typing\.Optional\[(?:bool|int)\]\n        [^\n]*\n"
)

# file (relative to src/axilio) -> regexes whose matches are deleted.
PATTERNS: dict[str, list[str]] = {
    "client.py": [
        _DOCSTRING,
        r"\n        stream_reconnection_enabled: typing\.Optional\[bool\] = None,",
        r"\n        max_stream_reconnection_attempts: typing\.Optional\[int\] = None,",
        r"\n            stream_reconnection_enabled=stream_reconnection_enabled,",
        r"\n            max_stream_reconnection_attempts=max_stream_reconnection_attempts,",
    ],
    "core/client_wrapper.py": [
        r"\n        stream_reconnection_enabled: typing\.Optional\[bool\] = None,",
        r"\n        max_stream_reconnection_attempts: typing\.Optional\[int\] = None,",
        r"\n            stream_reconnection_enabled=stream_reconnection_enabled,",
        r"\n            max_stream_reconnection_attempts=max_stream_reconnection_attempts,",
        r"\n        self\._stream_reconnection_enabled = stream_reconnection_enabled",
        r"\n        self\._max_stream_reconnection_attempts = max_stream_reconnection_attempts",
        r"\n    def get_stream_reconnection_enabled\(self\) -> bool:\n(?:        [^\n]*\n)+",
        r"\n    def get_max_stream_reconnection_attempts\(self\) -> typing\.Optional\[int\]:\n(?:        [^\n]*\n)+",
    ],
    "core/request_options.py": [
        r"\n    stream_reconnection_enabled: NotRequired\[bool\]",
        r"\n    max_stream_reconnection_attempts: NotRequired\[int\]",
    ],
}

# The argus client is a second generated Fern API with the same surface.
for rel in ("client.py", "core/client_wrapper.py", "core/request_options.py"):
    PATTERNS[f"argus/{rel}"] = PATTERNS[rel]


def main() -> int:
    for rel, patterns in PATTERNS.items():
        path = SRC / rel
        src = path.read_text()
        for pat in patterns:
            regex = re.compile(pat)
            matched = regex.search(src)
            if not matched:
                print(
                    f"strip_dead_stream_options: {rel}: pattern {pat!r} matched nothing - "
                    "the generator's shape changed; update this strip or re-decide the deletion",
                    file=sys.stderr,
                )
                return 1
            src = regex.sub("", src)
        path.write_text(src)
    print("stripped dead stream-reconnect options")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
