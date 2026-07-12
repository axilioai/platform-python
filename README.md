# Axilio Python SDK

The official Python SDK for [Axilio](https://axilio.ai). Acquire a mobile device
in the cloud and drive it with a clean, chainable API — find on-screen text and
elements, tap, swipe, type, and screenshot — plus typed access to workflows,
runs, usage, and billing.

## Installation

```bash
pip install axilio
```

Requires Python 3.10+.

## Quick start

```python
from axilio.platform import Client

client = Client()  # reads AXILIO_API_KEY from the environment

# Acquire a device, drive it, and release it automatically.
with client.session("ANDROID") as driver:
    driver.find_text("Settings").tap()
    driver.find(query="the blue Continue button").tap()

    png = driver.screenshot()  # bytes (PNG)
```

`Client` is the entry point: construct it once and share it. `client.session(...)`
acquires a device, opens the control channel, hands you a `MobileDriver`, and
releases the device when the `with` block exits. The rest of the API hangs off
the client as typed resource groups — `client.devices`, `client.runs`,
`client.workflows`, `client.billing`, and so on.

## Driving a device

The driver is built around **selectors** that return an `Element` you act on:

```python
with client.session("ANDROID") as driver:
    # Deterministic text selectors (fast, on-device OCR).
    driver.find_text("Settings").tap()
    driver.find_text("Search").type_into("axilio")

    # Natural-language selector (vision model) for anything text can't pin down.
    driver.find(query="the heart icon next to the comment count").tap()

    # find_all_text returns every match.
    for el in driver.find_all_text(contains="Notification"):
        print(el.text, el.center)  # {"x": .., "y": ..}

    # Snapshot the screen once, then query it without re-capturing.
    screen = driver.observe()
    print(len(screen.texts), len(screen.icons))

    # Wait for the UI to settle.
    driver.wait_for_text("Welcome")
    driver.wait_until_gone("Loading")
```

`find_text(text)` returns an `Element` or `None` (no match); `find(query=...)`
raises `ElementNotFoundError` if it can't locate the target. An `Element`'s
actions chain — `tap()`, `long_press(duration_ms=…)`, `type_into(text)`,
`swipe_to(other)` — and it carries `bbox`, `center`, `text`, `confidence`, and
`source` (`"ocr"` or `"vlm"`).

### Low-level input

When you already know the coordinates, drive the device directly:

```python
driver.tap({"x": 540, "y": 1180})
driver.swipe({"x": 540, "y": 1600}, {"x": 540, "y": 400})
driver.type_text("hello")

from axilio.drivers.mobile import Key
driver.key_press(Key.ENTER)  # submits / fires the keyboard's Go action (ENTER is the only named key today)
```

### Picking a device

`client.session("ANDROID")` claims a device from your shared pool. To pin a
specific **dedicated** device, pass its `phone_id`:

```python
mine = client.devices.mine()
with client.session("ANDROID", phone_id=mine.phones[0].phone_id) as driver:
    ...
```

## Authentication

```bash
export AXILIO_API_KEY=axl_...
```

Or pass it explicitly:

```python
client = Client(api_key="axl_...")
```

Generate keys from the [Axilio dashboard](https://app.axilio.ai/settings/api-keys).
The key is sent as the `X-Axilio-Api-Key` header. Each key is scoped to one
organization — if you belong to several, mint one key per org.

## Resources

Each group hangs off the client and returns typed responses. Highlights:

| Group | What it does | Example methods |
|---|---|---|
| `client.devices` | Acquire and inspect phones | `available()`, `mine()`, `allocate()`, `deallocate()`, `counts()`, `list_sessions()` |
| `client.runs` | Workflow runs | `create()`, `get()`, `list()`, `cancel()`, `list_events()` |
| `client.workflows` | Workflow CRUD + code | `list()`, `get()`, `create()`, `update()`, `get_code()`, `save_code()` |
| `client.usage` | Usage + metrics | `get_metrics()`, `list_sessions()`, `list_inferences()` |
| `client.billing` | Balance, subscription, invoices | `get_balance()`, `get_subscription()`, `get_history()`, `add_funds()` |
| `client.argus` | Vision inference (OCR + element detection) | `infer()`, `locate()`, `list_models()` |
| `client.api_keys` | Manage API keys | `list()`, `create()`, `regenerate()`, `delete()` |
| `client.org` | Organization + members | `get()`, `list_members()`, `create_invitation()`, `remove_member()` |
| `client.user` | The calling user | `get_me()`, `delete_me()` |

The generated client is available as `client.raw` (an `AxilioApi`) if you need a
method not surfaced here, or the async variant via `from axilio import
AsyncAxilioApi` (both are exported from the top-level `axilio` package).

## Errors

**REST calls** raise `axilio.ApiError` on a non-2xx response — inspect
`status_code` and `body`:

```python
from axilio.platform import ApiError

try:
    run = client.runs.get("run_123")
except ApiError as e:
    if e.status_code == 404:
        print("run not found")
    elif e.status_code == 429:
        ...  # back off and retry
    else:
        raise
```

**Device-control** calls raise typed exceptions from `axilio.drivers.mobile`,
all of which subclass its `AxilioError`:

```python
from axilio.drivers.mobile import ElementNotFoundError, TimeoutError

with client.session("ANDROID") as driver:
    try:
        driver.find(query="a button that isn't there", timeout=5).tap()
    except ElementNotFoundError:
        ...
    except TimeoutError:
        ...
```

Others include `ConnectionError`, `DeviceOfflineError`, `NotConnectedError`,
`InvalidArgsError`, and `UnauthorizedError`.

## Configuration

| Constructor kwarg | Default | Description |
|---|---|---|
| `api_key` | `AXILIO_API_KEY` env | Your API key (`axl_…`). |
| `base_url` | `AXILIO_BASE_URL` env, then `https://api.axilio.ai` | API host. |
| `timeout` | `30.0` | Per-request timeout, in seconds. |
| `max_retries` | `3` | Extra attempts on `429`/`5xx`/network errors before giving up. |

| Env var | Description |
|---|---|
| `AXILIO_API_KEY` | API key used to authenticate. |
| `AXILIO_BASE_URL` | Override the API host. |

Requests that fail with `429`, a `5xx`, or a transport-level error are retried
automatically with exponential backoff, up to `max_retries`; a `Retry-After`
response header takes precedence over the computed backoff. Other `4xx`
responses fail fast.

## Status

Axilio is in early access and the SDK surface is still expanding. APIs may
change between minor versions until 1.0 — pin a version for reproducible builds.

## Roadmap

- **Live run events** — REST polling today; streaming subscriptions to come.
