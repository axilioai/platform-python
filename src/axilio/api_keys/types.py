"""Public types for API key management."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class APIKey:
    """An API key as listed. `prefix` is the first 8 chars of the key
    for identification — the full secret is never returned by list().
    Use APIKeyCreated.secret on create() to get the plaintext once."""

    id: str
    name: str
    prefix: str
    created_at: datetime
    last_used_at: datetime | None


@dataclass(frozen=True)
class APIKeyCreated:
    """Returned by create() only. The `secret` is the only chance the
    caller has to see the plaintext — the backend stores a hash and
    list() won't return it. Treat as write-once."""

    id: str
    name: str
    secret: str
    prefix: str
    created_at: datetime
