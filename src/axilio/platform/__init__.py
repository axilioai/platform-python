"""Axilio platform client — the ergonomic entry point for the REST API.

A thin wrapper over the Fern-generated ``AxilioApi``. The generated client
owns the wire (typed requests/responses, retries, ``X-Axilio-Api-Key`` auth);
this layer adds the ergonomics it doesn't:

* resolves the API key from ``api_key=`` / ``AXILIO_API_KEY`` (falling back to
  ``AXILIO_SANDBOX_TOKEN`` when running inside a sandbox),
* defaults and normalises the base URL,
* detects local-vs-sandbox mode, and
* exposes the generated resource groups (``phones``, ``runs``, ``workflows``…).

Hand-written and preserved across ``fern generate`` via ``src/axilio/.fernignore``.
"""

from __future__ import annotations

import contextlib
import os
from collections.abc import Iterator

from .. import AxilioApi
from .._config import load_api_key, load_base_url
from .._mode import Mode, detect
from ..argus import ArgusApi
from ..core.api_error import ApiError
from ..drivers.mobile import MobileDriver

# Re-export ApiError here so callers get the whole public REST surface from one
# namespace — `from axilio.platform import Client, ApiError`. It otherwise lives
# under the Fern-generated `axilio.core`, which is regenerated wholesale on every
# `fern generate`; this module is in .fernignore, so the alias is stable.
__all__ = ["ApiError", "Client", "MobileDriver"]

DEFAULT_BASE_URL = "https://api.axilio.ai"

# Argus (vision inference) runs on its own host, and its OpenAPI paths already
# include the full "/api/v1/inference" prefix, so its base URL is the bare host
# with no _API_PREFIX appended. Kept separate from the backend client on purpose
# (see axilio/argus). Override per environment with AXILIO_ARGUS_BASE_URL.
DEFAULT_ARGUS_BASE_URL = "https://argus.axilio.ai"

# The OpenAPI spec declares a "/api/v1" server and its paths are bare
# ("/devices/allocate"), so the generated client needs that prefix folded
# into its base_url. We keep the public base_url host-only (what callers and
# AXILIO_BASE_URL set) and append the prefix when constructing the client.
_API_PREFIX = "/api/v1"

_ENV_API_KEY = "AXILIO_API_KEY"
_ENV_BASE_URL = "AXILIO_BASE_URL"
_ENV_ARGUS_BASE_URL = "AXILIO_ARGUS_BASE_URL"
_ENV_SANDBOX_TOKEN = "AXILIO_SANDBOX_TOKEN"


class Client:
    """Top-level Axilio client. Construct once per process and share across calls."""

    def __init__(
        self,
        *,
        api_key: str | None = None,
        base_url: str | None = None,
        argus_base_url: str | None = None,
        timeout: float = 30.0,
        max_retries: int = 3,
    ) -> None:
        self._mode = detect()
        resolved_key = (
            api_key
            or os.environ.get(_ENV_API_KEY)
            or load_api_key()  # persisted by `axilio login`
            or (os.environ.get(_ENV_SANDBOX_TOKEN) if self._mode is Mode.SANDBOX else None)
        )
        if not resolved_key:
            raise ValueError(
                "API key not provided. Pass api_key=... or set the "
                f"{_ENV_API_KEY} environment variable."
            )
        self._api_key = resolved_key
        self._base_url = (
            base_url or os.environ.get(_ENV_BASE_URL) or load_base_url() or DEFAULT_BASE_URL
        ).rstrip("/")
        self._api = AxilioApi(
            api_key=resolved_key,
            base_url=self._base_url + _API_PREFIX,
            timeout=timeout,
            max_retries=max_retries,
        )
        # Argus is a separate service/host; its paths already carry /api/v1, so the
        # base URL is the bare host (no _API_PREFIX).
        self._argus_base_url = (
            argus_base_url or os.environ.get(_ENV_ARGUS_BASE_URL) or DEFAULT_ARGUS_BASE_URL
        ).rstrip("/")
        self._argus = ArgusApi(
            api_key=resolved_key,
            base_url=self._argus_base_url,
            timeout=timeout,
            max_retries=max_retries,
        )

    # --- resource groups (delegated to the generated client) ---------------
    @property
    def phones(self):  # noqa: ANN201 — returns the generated PhonesClient
        return self._api.phones

    @property
    def devices(self):  # noqa: ANN201 — back-compat alias for `phones`
        return self._api.phones

    @property
    def mobile(self):  # noqa: ANN201 — back-compat alias for `phones`
        return self._api.phones

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
    def argus(self):  # noqa: ANN201 — vision inference: infer / locate / list_models
        return self._argus.inference

    @property
    def api_keys(self):  # noqa: ANN201
        return self._api.api_keys

    @property
    def org(self):  # noqa: ANN201 — generated group is named `organizations`
        return self._api.organizations

    @property
    def user(self):  # noqa: ANN201
        return self._api.user

    # --- device control ----------------------------------------------------
    @contextlib.contextmanager
    def session(
        self,
        phone_type: str = "ANDROID",
        *,
        phone_id: str | None = None,
        workflow_id: str | None = None,
        open_timeout: float = 10.0,
        default_ocr_engine: str | None = None,
        default_model: str | None = None,
    ) -> Iterator[MobileDriver]:
        """Acquire a device and yield a connected ``MobileDriver``, releasing on exit.

        Remote (local / CI usage): allocates a device, dials its DCP control URL,
        and deallocates when the ``with`` block exits::

            with client.session("android") as driver:
                driver.find(query="the search box").tap()
                driver.screenshot()

        Sandbox: inside an Axilio sandbox the device is pre-allocated on the
        daemon socket, so allocation is skipped and the local transport is used —
        the same script drives both transports unchanged.

        ``default_ocr_engine`` / ``default_model`` become the driver's
        session-wide defaults for the vision calls: every ``ocr_engine=`` /
        ``model=`` kwarg not passed per call falls back to them, so
        ``client.session(default_ocr_engine="premium")`` upgrades a whole
        session without repeating the kwarg. A per-call argument always wins.
        See ``GET /vision/models`` (or the Models docs page) for the
        available engines, model ids, and pricing.
        """
        # Sandbox shortcut: a pre-allocated device reachable on the daemon socket.
        if self._mode is Mode.SANDBOX:
            driver = MobileDriver.connect(
                default_ocr_engine=default_ocr_engine,
                default_model=default_model,
            )
            try:
                yield driver
            finally:
                with contextlib.suppress(Exception):
                    driver.close()
            return

        # Remote: allocate → drive → release. Normalize the phone type to the
        # backend enum casing (ANDROID/IOS) so callers can pass "android" too.
        alloc_kwargs: dict[str, str] = {"phone_type": phone_type.strip().upper()}
        if phone_id is not None:
            alloc_kwargs["phone_id"] = phone_id
        if workflow_id is not None:
            alloc_kwargs["workflow_id"] = workflow_id
        alloc = self._api.phones.allocate(**alloc_kwargs)
        # Once allocate succeeds the device is reserved, so deallocate must run on
        # every exit path below — including the no-control_url error — or we leak it.
        try:
            if not alloc.control_url:
                raise RuntimeError(
                    "allocation returned no control_url — device control is not "
                    "available in this environment (is the connect service deployed?)"
                )
            driver = MobileDriver.connect_remote(
                alloc.control_url,
                open_timeout=open_timeout,
                default_ocr_engine=default_ocr_engine,
                default_model=default_model,
            )
            try:
                yield driver
            finally:
                with contextlib.suppress(Exception):
                    driver.close()
        finally:
            with contextlib.suppress(Exception):
                self._api.phones.deallocate(phone_id=alloc.phone_id)

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
