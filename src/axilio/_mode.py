"""Local vs sandbox mode detection."""

from __future__ import annotations

import os
from enum import Enum

_SANDBOX_TOKEN_ENV = "AXILIO_SANDBOX_TOKEN"
_SANDBOX_ATLAS_ENV = "AXILIO_ATLAS_ENDPOINT"


class Mode(str, Enum):
    LOCAL = "local"
    SANDBOX = "sandbox"


def detect() -> Mode:
    """Inspect the environment and return the active mode (sandbox needs both env vars)."""
    if os.environ.get(_SANDBOX_TOKEN_ENV) and os.environ.get(_SANDBOX_ATLAS_ENV):
        return Mode.SANDBOX
    return Mode.LOCAL
