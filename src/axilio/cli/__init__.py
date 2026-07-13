"""The ``axilio`` command-line interface.

Hand-written; preserved across ``fern generate`` via ``src/axilio/.fernignore``.
Thin ergonomics over the SDK: one-command auth (``login``), imperative phone-session
control (``session start|status|stop``), and an environment check (``doctor``).
Run ``axilio --help``.
"""

from ._app import main

__all__ = ["main"]
