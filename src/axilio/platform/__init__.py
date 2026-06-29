"""Axilio platform client — the ergonomic entry point for the REST API.

A thin wrapper over the Fern-generated ``AxilioApi``. The generated client
owns the wire (typed requests/responses, retries, ``X-Axilio-Api-Key`` auth);
this layer adds the ergonomics it doesn't:

* resolves the API key from ``api_key=`` / ``AXILIO_API_KEY`` (falling back to
  ``AXILIO_SANDBOX_TOKEN`` when running inside a sandbox),
* defaults and normalises the base URL,
* detects local-vs-sandbox mode, and
* exposes the generated resource groups (``devices``, ``runs``, ``workflows``…).

Hand-written and preserved across ``fern generate`` via ``src/axilio/.fernignore``.
"""

from __future__ import annotations

import contextlib
import os

from .. import AxilioApi
from .._mode import Mode, detect

DEFAULT_BASE_URL = "https://api.axilio.ai"

# The OpenAPI spec declares a "/api/v1" server and its paths are bare
# ("/devices/allocate"), so the generated client needs that prefix folded
# into its base_url. We keep the public base_url host-only (what callers and
# AXILIO_BASE_URL set) and append the prefix when constructing the client.
_API_PREFIX = "/api/v1"

_ENV_API_KEY = "AXILIO_API_KEY"
_ENV_BASE_URL = "AXILIO_BASE_URL"
_ENV_SANDBOX_TOKEN = "AXILIO_SANDBOX_TOKEN"


class Client:
    """Top-level Axilio client. Construct once per process and share across calls."""

    def __init__(
        self,
        *,
        api_key: str | None = None,
        base_url: str | None = None,
        timeout: float = 30.0,
        max_retries: int = 3,
    ) -> None:
        self._mode = detect()
        resolved_key = (
            api_key
            or os.environ.get(_ENV_API_KEY)
            or (os.environ.get(_ENV_SANDBOX_TOKEN) if self._mode is Mode.SANDBOX else None)
        )
        if not resolved_key:
            raise ValueError(
                "API key not provided. Pass api_key=... or set the "
                f"{_ENV_API_KEY} environment variable."
            )
        self._api_key = resolved_key
        self._base_url = (base_url or os.environ.get(_ENV_BASE_URL) or DEFAULT_BASE_URL).rstrip("/")
        self._api = AxilioApi(
            api_key=resolved_key,
            base_url=self._base_url + _API_PREFIX,
            timeout=timeout,
            max_retries=max_retries,
        )

    # --- resource groups (delegated to the generated client) ---------------
    @property
    def devices(self):  # noqa: ANN201 — returns the generated DevicesClient
        return self._api.devices

    @property
    def mobile(self):  # noqa: ANN201 — back-compat alias for `devices`
        return self._api.devices

    @property
    def runs(self):  # noqa: ANN201
        return self._api.runs

    @property
    def workflows(self):  # noqa: ANN201
        return self._api.workflows

    @property
    def usage(self):  # noqa: ANN201
        return self._api.usage

    @property
    def billing(self):  # noqa: ANN201
        return self._api.billing

    @property
    def api_keys(self):  # noqa: ANN201
        return self._api.api_keys

    @property
    def org(self):  # noqa: ANN201 — generated group is named `organizations`
        return self._api.organizations

    @property
    def user(self):  # noqa: ANN201
        return self._api.user

    @property
    def user_settings(self):  # noqa: ANN201
        return self._api.user_settings

    # --- introspection -----------------------------------------------------
    @property
    def raw(self) -> AxilioApi:
        """The underlying Fern-generated client — an escape hatch for callers
        that need a resource group not surfaced here, or the async variant."""
        return self._api

    @property
    def base_url(self) -> str:
        return self._base_url

    @property
    def api_key(self) -> str:
        return self._api_key

    @property
    def mode(self) -> Mode:
        """Local vs sandbox — auto-detected from the environment at construction."""
        return self._mode

    def close(self) -> None:
        """Release the underlying HTTP connection pool."""
        with contextlib.suppress(Exception):
            self._api._client_wrapper.httpx_client.httpx_client.close()

    def __enter__(self) -> Client:
        return self

    def __exit__(self, *_: object) -> None:
        self.close()


__all__ = ["Client"]
