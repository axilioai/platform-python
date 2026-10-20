"""Local vs sandbox mode detection."""

from __future__ import annotations

import os
from enum import Enum

# Where an Axilio workflow sandbox serves its pre-allocated phone. The socket is
# the only thing the sandbox provides the SDK: it sets no environment variable
# of its own, so its presence is what makes a process "in a sandbox".
DEFAULT_SOCKET_PATH = "/run/axilio/sdk.sock"
SOCKET_PATH_ENV = "AXILIO_SDK_SOCKET"


class Mode(str, Enum):
    LOCAL = "local"
    SANDBOX = "sandbox"


def socket_path() -> str:
    """The sandbox SDK socket: ``AXILIO_SDK_SOCKET``, else the default path."""
    return os.environ.get(SOCKET_PATH_ENV) or DEFAULT_SOCKET_PATH


def detect() -> Mode:
    """SANDBOX when the sandbox's SDK socket exists, else LOCAL."""
    return Mode.SANDBOX if os.path.exists(socket_path()) else Mode.LOCAL
