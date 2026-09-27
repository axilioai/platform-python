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

The task-first walkthrough lives in the
[SDK quickstart](https://docs.axilio.ai/quickstart): install, authenticate,
allocate a real Android phone, inspect its screen, and release it. The same
flow in one file:

```python
from pathlib import Path

from axilio.platform import Client

client = Client()  # reads AXILIO_API_KEY from the environment

# session() allocates a phone, connects a driver, and releases the phone when
# the block exits, on the normal path and when the code raises.
with client.session("android") as driver:
    screen = driver.observe()
    print(f"Found {len(screen.texts)} text regions and {len(screen.icons)} icons")

    Path("screen.png").write_bytes(driver.screenshot())
```

`Client` is the entry point: construct it once and share it. `client.session(...)`
acquires a device, opens the control channel, hands you a `MobileDriver`, and
releases the device when the `with` block exits. The rest of the API hangs off
the client as typed resource groups — `client.phones`, `client.runs`,
`client.workflows`, `client.billing`, and so on.

## Driving a device

The driver is built around **locators**: Playwright-style, lazy handles on a
target. Building one sends nothing; an action or query resolves it against
*whatever's on screen at that moment*, auto-waits until it's actionable, and
(for `tap`/`fill`/`press`) acts, all in one round trip:

```python
with client.session("android") as driver:
    # Deterministic text selector (fast, on-device OCR).
    driver.get_by_text("Settings").tap()
    driver.get_by_text("Search").fill("axilio")

    # Natural-language selector (vision model) for anything text can't pin down.
    driver.locator(query="the heart icon next to the comment count").tap()

    # Refine with nth / within / has / filter; each returns a new locator.
    driver.get_by_text("Card").has(driver.get_by_text("Free shipping")).nth(0).tap()

    # Wait for the UI to settle.
    driver.get_by_text("Welcome").wait_for()
    driver.get_by_text("Loading").wait_for(state="hidden")

    # Snapshot the screen once, then query it without re-capturing.
    screen = driver.observe()
    print(len(screen.texts), len(screen.icons))
```

A locator's actions and queries (`tap()`, `fill(text)`, `press(key)`,
`wait_for(state=…)`, `bounding_box()`, `text()`, `count()`) take only
`timeout=` and each return a `LocatorResult` (`resolved_by`, `bounds`,
`took_ms`, `model_name`) or, for `text()`/`count()`, a plain `str`/`int`.
`get_by_text(text, exact=False)` resolves by OCR; `get_by_role(role,
name=...)` / `get_by_id(id)` need the accessibility tree and raise
`StrategyUnavailableError` on a phone that doesn't expose one (every phone
today); `locator(query=...)` is read by a vision model. A timed-out
auto-wait raises `ActionTimeoutError` (also catchable as the builtin
`TimeoutError`). `count()` is the one call that never waits: it reports how
many targets match the current screen right now, zero included, so use
`wait_for()` to wait for something to appear. `count()` also needs a plain
text locator; one that also carries `query`, `within`, or `has` raises
`InvalidArgsError`.

`locator(...)`, `get_by_text(...)`, `get_by_role(...)`, and `get_by_id(...)`
each take `model=`, `ocr_engine=`, and `strategy=`, keyword-only: these
resolution options live on the locator, not on the action, since the
locator is what resolves the target. Unset, each falls back to the driver's
`default_model` / `default_ocr_engine` / `default_strategy`, then is omitted
from the wire. A refinement (`nth()`, `first()`, `within()`, `has()`,
`filter()`) keeps whatever options the locator it's called on was built
with:

```python
strict = driver.get_by_text("Save", strategy="accessibility")
strict.nth(0).tap()  # still resolves with strategy="accessibility"
```

`within(other)` and `has(other)` only take `other`'s selector fields into
the scope; `other`'s own `model`/`ocr_engine`/`strategy` are ignored, since
the outer locator's options govern the whole call. The edge resolves the
whole locator, scopes included, in one round trip. On the vision path (no
accessibility tree, which is every phone today), a plain `text` locator is
still an OCR match, but a locator with `query`, `within`, `has`, or `nth`
is resolved by one vision-model call instead, with a prompt built from the
whole locator; `nth` works the same way on a `query` locator as on a plain
one.

`observe()` still returns a `Screen`: a plain, already-captured snapshot with
`Screen.find_text` / `Screen.find_all_text` as pure data filters over it (no
re-fetch, no actions attached); reach for a locator instead when you're about
to act on something.

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

`client.session("android")` claims a device from your shared pool. To pin a
specific **dedicated** device, pass its `phone_id`:

```python
mine = client.phones.mine()
with client.session("android", phone_id=mine.phones[0].phone_id) as driver:
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
| `client.phones` | Acquire and inspect phones | `available()`, `mine()`, `allocate()`, `deallocate()`, `list_sessions()` |
| `client.runs` | Workflow runs | `create()`, `get()`, `list()`, `cancel()`, `list_events()` |
| `client.workflows` | Workflow CRUD + code | `list()`, `get()`, `create()`, `update()`, `get_code()`, `save_code()` |
| `client.usage` | Usage + metrics | `get_metrics()`, `list_inferences()` |
| `client.billing` | Balance, subscription, invoices | `get_balance()`, `get_subscription()`, `get_history()` |
| `client.argus` | Vision (OCR + element detection) | `detect()`, `locate()`, `list_models()` |
| `client.api_keys` | Manage API keys | `list()`, `create()`, `regenerate()`, `delete()` |

Organization and user account management aren't exposed here by design — use the
dashboard for those.

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
from axilio.drivers.mobile import ActionTimeoutError, StrategyUnavailableError

with client.session("android") as driver:
    try:
        driver.locator(query="a button that isn't there").tap(timeout=5)
    except ActionTimeoutError:
        ...  # never became actionable within the budget (also a builtin TimeoutError)
    except StrategyUnavailableError:
        ...  # the resolver needs a capability this session doesn't have
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
