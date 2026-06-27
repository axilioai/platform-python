"""Axilio Python SDK — ``axilio.platform`` (the Client) + ``axilio.drivers`` (device drivers)."""

from __future__ import annotations

from ._errors import (
    AllocationMismatchError,
    AxilioError,
    NotFoundError,
    RateLimitError,
    SandboxPermissionError,
    ServerError,
    UnauthorizedError,
)

__all__ = [
    "AxilioError",
    "UnauthorizedError",
    "RateLimitError",
    "NotFoundError",
    "ServerError",
    "SandboxPermissionError",
    "AllocationMismatchError",
]
