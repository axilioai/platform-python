# Axilio Python SDK

The official Python SDK for [Axilio](https://axilio.ai). Acquire a mobile device in the cloud and drive it with a clean, chainable API — find on-screen text and elements, tap, swipe, type, and screenshot — plus account, usage, and billing management.

## Installation

```bash
pip install axilio
```

Requires Python 3.10+.

## Quick start

```python
from axilio.platform import Client
from axilio.drivers import MobileDriver

client = Client()  # reads AXILIO_API_KEY from the environment

# Acquire a device, drive it, and release it automatically.
with client.mobile.session(platform="android") as device:
    driver = MobileDriver(device)

    driver.find_text("Sign in").tap()
    driver.find_text("Email").type_into("you@example.com")
    driver.find(query="the blue Continue button").tap()

    png = driver.screenshot()
```

`client.mobile` acquires a device and hands you a `DeviceHandle`; you wrap it
with a `MobileDriver` to control it. The platform client acquires the device,
the driver drives it.

### Driving a device

The driver is built around **selectors** that return an `Element` you act on:

```python
# Deterministic text selectors (fast, on-device OCR).
driver.find_text("Settings").tap()
driver.find_all_text(contains="Notification")

# Natural-language selector (vision model) for anything text can't pin down.
driver.find(query="the heart icon next to the comment count").tap()

# Snapshot the screen once, then query it without re-capturing.
screen = driver.observe()
print(len(screen.texts), len(screen.icons))
screen.find_text("Done").tap()

# Wait for the UI to settle.
driver.wait_for_text("Welcome")
driver.wait_until_gone("Loading")
```

Every selector returns an `Element` whose actions chain: `tap()`,
`long_press()`, `type_into(text)`, `swipe_to(other)`.

## Authentication

```bash
export AXILIO_API_KEY=ax_live_...
```

Or pass it explicitly:

```python
client = Client(api_key="ax_...")
```

Generate keys from the [Axilio dashboard](https://app.axilio.ai/settings/api-keys). Each API key is scoped to one organization — if you belong to several, mint one key per org.

## Resources

| Resource | Methods |
|---|---|
| `client.mobile` | `available()`, `locations()`, `supported_apps()`, `allocate()`, `deallocate()`, `session()` |
| `client.workflows` | `list()`, `get()`, `create()`, `update()`, `delete()` |
| `client.runs` | `list()`, `get()`, `create()`, `cancel()` |
| `client.usage` | `metrics()`, `sessions()` |
| `client.billing` | `balance()`, `subscription()`, `invoices()`, `upgrade()`, `downgrade()` |
| `client.api_keys` | `list()`, `create()`, `revoke()` |
| `client.org` | `current()`, `members()`, `invite()`, `remove_member()` |

`client.mobile.allocate()` (and `session()`) return a `DeviceHandle`; wrap it
with `axilio.drivers.MobileDriver` to control the device.

## Errors

Every error raised by the SDK subclasses `axilio.AxilioError`, so you can catch
broadly or handle specific cases:

```python
from axilio.platform import Client, NotFoundError, RateLimitError

client = Client()

try:
    run = client.runs.get("run_123")
except NotFoundError:
    print("run not found")
except RateLimitError:
    ...  # back off and retry
```

| Exception | HTTP | Meaning |
|---|---|---|
| `UnauthorizedError` | 401 | API key missing, malformed, or rejected |
| `NotFoundError` | 404 | Resource doesn't exist or isn't visible to your key |
| `RateLimitError` | 429 | Retry after a backoff |
| `ServerError` | 5xx | Transient; safe to retry |
| `AxilioError` | — | Base class / catch-all |

## Configuration

| Env var | Description |
|---|---|
| `AXILIO_API_KEY` | API key used to authenticate. |
| `AXILIO_BASE_URL` | Override the API host (defaults to `https://api.axilio.ai`). |

| Constructor kwarg | Default | Description |
|---|---|---|
| `api_key` | `AXILIO_API_KEY` env | Your API key. |
| `base_url` | `AXILIO_BASE_URL` env, then `https://api.axilio.ai` | API host. |
| `timeout` | `30.0` | Per-request timeout, in seconds. |
| `max_retries` | `3` | Extra attempts on `429`/`5xx`/network errors before giving up. Set `0` to disable. |
| `retry_base_delay` | `0.5` | Base seconds for exponential backoff between retries. |

### Retries

Requests that fail with `429` (rate limited), a `5xx` (transient backend
error), or a transport-level error (connection refused/reset, timeout) are
retried automatically — up to `max_retries` extra attempts with exponential
backoff and jitter. A `Retry-After` response header, when present, takes
precedence over the computed backoff. Other `4xx` responses (bad request, not
found, unauthorized) fail fast, since replaying them won't change the outcome.

## Status

Axilio is in early access and the SDK surface is still expanding. APIs may
change between minor versions until 1.0 — pin a version for reproducible
builds.

## Roadmap

- **Async client** — synchronous only today.
- **Live run events** — REST polling today; streaming subscriptions to come.
