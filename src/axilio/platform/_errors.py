"""Typed REST errors the platform layer raises on top of ``ApiError``.

The generated client raises a plain ``ApiError`` for every non-2xx. Where the
backend puts a stable token at the front of a problem's ``detail`` so clients
can match on it rather than on prose, this module turns that one response
into a subclass, so ``except ApiError`` keeps catching it and a caller who
cares can catch the narrower type.
"""

from __future__ import annotations

import typing

from ..core.api_error import ApiError

# Why a session ended, as the backend's session.ended webhook reports it
# (``end_reason``). accessibility_unavailable: the phone could not confirm
# the session's accessibility state before handover, so the platform ended
# the session and returned the phone to the pool.
SessionEndReason = typing.Literal[
    "released",
    "idle_timeout",
    "max_duration",
    "run_finished",
    "device_lost",
    "accessibility_unavailable",
]

_ACCESSIBILITY_UNAVAILABLE = "accessibility_unavailable"


class AccessibilityUnavailableError(ApiError):
    """Allocation asked for ``accessibility=True`` and named a ``phone_id``
    that can't run accessibility mode (HTTP 409).

    An exhausted pool (no free phone that supports it) is the ordinary
    no-phone 409 instead, an ``ApiError``, exactly as without the flag.
    """


def _problem_detail(body: typing.Any) -> str:
    if isinstance(body, dict):
        detail = body.get("detail")
        if isinstance(detail, str):
            return detail
    return ""


def map_allocate_error(e: ApiError) -> ApiError:
    """The typed error for an allocate failure, or ``e`` itself."""
    if e.status_code == 409 and _problem_detail(e.body).startswith(
        _ACCESSIBILITY_UNAVAILABLE + ":"
    ):
        return AccessibilityUnavailableError(
            headers=e.headers, status_code=e.status_code, body=e.body
        )
    return e
