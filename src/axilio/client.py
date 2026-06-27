"""Axilio Client — the entry point for everything in the SDK."""

from __future__ import annotations

import os

from . import _mode
from ._http import HTTPClient
from .api_keys import APIKeysResource
from .argus import ArgusResource
from .billing import BillingResource
from .devices import MobileResource
from .org import OrgResource
from .runs import RunsResource
from .usage import UsageResource
from .workflows import WorkflowsResource

DEFAULT_BASE_URL = "https://api.axilio.ai"
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
        retry_base_delay: float = 0.5,
    ) -> None:
        self._mode = _mode.detect()
        resolved_key = (
            api_key
            or os.environ.get(_ENV_API_KEY)
            or (os.environ.get(_ENV_SANDBOX_TOKEN) if self._mode is _mode.Mode.SANDBOX else None)
        )
        if not resolved_key:
            raise ValueError(
                "API key not provided. Pass api_key=... or set the "
                f"{_ENV_API_KEY} environment variable."
            )
        self._api_key = resolved_key
        self._base_url = (base_url or os.environ.get(_ENV_BASE_URL) or DEFAULT_BASE_URL).rstrip("/")
        self._http = HTTPClient(
            api_key=self._api_key,
            base_url=self._base_url,
            timeout=timeout,
            max_retries=max_retries,
            retry_base_delay=retry_base_delay,
        )

        self.billing = BillingResource(self._http, self._mode)
        self.usage = UsageResource(self._http, self._mode)
        self.api_keys = APIKeysResource(self._http, self._mode)
        self.org = OrgResource(self._http, self._mode)
        self.mobile = MobileResource(self._http, self._mode)
        self.workflows = WorkflowsResource(self._http, self._mode)
        self.runs = RunsResource(self._http, self._mode)
        self.argus = ArgusResource(self._http, self._mode)

    @property
    def base_url(self) -> str:
        return self._base_url

    @property
    def api_key(self) -> str:
        return self._api_key

    @property
    def mode(self) -> _mode.Mode:
        """Local vs sandbox — auto-detected from the environment at construction."""
        return self._mode

    def close(self) -> None:
        """Release the underlying HTTP connection pool."""
        self._http.close()

    def __enter__(self) -> Client:
        return self

    def __exit__(self, *_: object) -> None:
        self.close()
