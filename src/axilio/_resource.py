"""Shared base class for every domain resource.

Each resource (billing, devices, workflows, etc.) takes the same
two collaborators: the shared HTTPClient (for wire calls) and the
active Mode (so it can short-circuit allocations in sandbox mode
and refuse writes that aren't allowed there). Centralising the
constructor + the sandbox-write guard here keeps every concrete
resource module honest about the rules.
"""

from __future__ import annotations

from . import _mode
from ._errors import SandboxPermissionError
from ._http import HTTPClient


class _Resource:
    """Common scaffolding for every Client.<domain>. Not part of the
    public API — single-underscore on purpose."""

    def __init__(self, http: HTTPClient, mode: _mode.Mode) -> None:
        self._http = http
        self._mode = mode

    def _require_local_mode(self, operation: str) -> None:
        """Raise SandboxPermissionError when called inside a sandbox VM.
        Use on every write that the design doc marks local-only —
        billing upgrade/downgrade, api_keys.create/revoke, org.invite
        and remove_member, etc. Read methods don't call this."""
        if self._mode is _mode.Mode.SANDBOX:
            raise SandboxPermissionError(
                f"{operation} is only available in local mode; "
                "sandbox-executed code has a read-only account surface."
            )
