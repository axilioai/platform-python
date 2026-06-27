"""OrgResource — client.org.*"""

from __future__ import annotations

from .._resource import _Resource
from .types import Invitation, Member, Organization, Role


class OrgResource(_Resource):
    """client.org — current org info + membership."""

    def current(self) -> Organization:
        """The org this API key is scoped to. Read; both modes."""
        raise NotImplementedError("OrgResource.current — codegen pending")

    def members(self) -> list[Member]:
        """All members of the current org. Read; both modes."""
        raise NotImplementedError("OrgResource.members — codegen pending")

    def invite(self, email: str, role: Role) -> Invitation:
        """Invite a user to the org. Local-mode only — sandbox scripts
        can't add new humans to the org they run for."""
        self._require_local_mode("org.invite")
        raise NotImplementedError("OrgResource.invite — codegen pending")

    def remove_member(self, user_id: str) -> None:
        """Remove a member from the org. Local-mode only."""
        self._require_local_mode("org.remove_member")
        raise NotImplementedError("OrgResource.remove_member — codegen pending")
