"""APIKeysResource — client.api_keys.*

All operations local-mode only. A scheduled script can't mint or
revoke API keys for its owner — that's strictly the user's surface.
"""

from __future__ import annotations

from .._resource import _Resource
from .types import APIKey, APIKeyCreated


class APIKeysResource(_Resource):
    """client.api_keys — list, create, revoke."""

    def list(self) -> list[APIKey]:
        """Active API keys for the current org. Local-mode only."""
        self._require_local_mode("api_keys.list")
        raise NotImplementedError("APIKeysResource.list — codegen pending")

    def create(self, name: str) -> APIKeyCreated:
        """Mint a new API key. The plaintext `secret` on the returned
        object is the only time it's visible — store it before
        discarding the object. Local-mode only."""
        self._require_local_mode("api_keys.create")
        raise NotImplementedError("APIKeysResource.create — codegen pending")

    def revoke(self, key_id: str) -> None:
        """Permanently revoke. The key stops authenticating
        immediately; in-flight requests carrying it complete
        normally. Local-mode only."""
        self._require_local_mode("api_keys.revoke")
        raise NotImplementedError("APIKeysResource.revoke — codegen pending")
