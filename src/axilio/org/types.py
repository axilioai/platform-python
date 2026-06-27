"""Public types for organization queries."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Literal

Role = Literal["viewer", "member", "admin", "owner"]


@dataclass(frozen=True)
class Organization:
    """The org the current API key is scoped to (keys are minted per-org)."""

    id: str
    name: str
    slug: str
    created_at: datetime
    onboarding_completed_at: datetime | None


@dataclass(frozen=True)
class Member:
    """One org member. Role is the customer-facing simplification of
    the backend's RBAC: viewer < member < admin < owner."""

    user_id: str
    email: str
    name: str
    role: Role
    joined_at: datetime


@dataclass(frozen=True)
class Invitation:
    """A pending invite. Created via invite() — the user accepts via
    an invite link the backend emails them."""

    id: str
    email: str
    role: Role
    invited_at: datetime
    expires_at: datetime
