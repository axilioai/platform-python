"""Persistent CLI credentials, shared by ``axilio login`` and ``Client`` resolution.

Hand-written and preserved across ``fern generate`` via ``src/axilio/.fernignore``.
``axilio login`` writes the API key here (0600); ``Client()`` falls back to it when
neither ``api_key=`` nor ``AXILIO_API_KEY`` is set, so a one-time login makes both
the CLI and the SDK "just work".
"""

from __future__ import annotations

import json
import os
import stat
from pathlib import Path

_APP_DIR = "axilio"
_FILE = "config.json"


def config_path() -> Path:
    """Location of the CLI config file, honouring ``XDG_CONFIG_HOME``."""
    base = os.environ.get("XDG_CONFIG_HOME") or os.path.join(Path.home(), ".config")
    return Path(base) / _APP_DIR / _FILE


def load_config() -> dict[str, str]:
    """Read the config file, returning ``{}`` if it is missing or unreadable."""
    try:
        with config_path().open(encoding="utf-8") as f:
            data = json.load(f)
    except (OSError, ValueError):
        return {}
    return data if isinstance(data, dict) else {}


def save_config(config: dict[str, str]) -> Path:
    """Write ``config`` as JSON, readable only by the owner (0600); returns the path."""
    path = config_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(config, f, indent=2)
        f.write("\n")
    os.chmod(path, stat.S_IRUSR | stat.S_IWUSR)
    return path


def load_api_key() -> str | None:
    """The stored API key, or ``None`` when none is saved."""
    return load_config().get("api_key") or None


def load_base_url() -> str | None:
    """The stored base-URL override, or ``None`` when none is saved."""
    return load_config().get("base_url") or None
