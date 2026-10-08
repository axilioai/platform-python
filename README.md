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
# accessibility=True turns on the accessibility tree that get_by_role and
# get_by_id read (see "Accessibility mode" below). It is off by default.
with client.session("android", accessibility=True) as driver:
    # Literal selectors: you write the text, role or id, the device matches it.
    driver.get_by_text("Settings").tap()
    driver.get_by_role("textbox", name="Search").fill("axilio")
    driver.get_by_id("com.example.app:id/login").tap()

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
`get_by_text(text, exact=False)` matches visible text, against the phone's
accessibility tree when the session has one and by OCR otherwise;
`locator(query=...)` is the one natural-language selector, ranked by a
model. A timed-out auto-wait raises `ActionTimeoutError`
(also catchable as the builtin `TimeoutError`). `count()` is the one call
that never waits: it reports how many targets match the current screen
right now, zero included, so use `wait_for()` to wait for something to
appear. `count()` also needs a plain text locator; one that also carries
`query`, `within`, or `has` raises `InvalidArgsError`.

Every locator constructor (`locator`, `get_by_text`, `get_by_role`,
`get_by_id`) takes `strategy=`, `model=` and `ocr_engine=`, keyword-only:
these resolution options live on the locator, not on the action, since the
locator is what resolves the target. Unset, each falls back to the driver's
`default_strategy` / `default_model` / `default_ocr_engine` (all three are
also `client.session(...)` arguments), then is omitted from the wire. A
refinement (`nth()`, `first()`, `within()`, `has()`, `filter()`) keeps
whatever options the locator it's called on was built with:

```python
premium = driver.get_by_text("Save", ocr_engine="premium")
premium.nth(0).tap()  # still resolves with ocr_engine="premium"
```

`within(other)` and `has(other)` only take `other`'s selector fields into
the scope; the outer locator's options govern the whole call, since the edge
resolves the whole locator, scopes included, in one round trip. If `other`
itself sets `strategy`, `model` or `ocr_engine` (as opposed to inheriting
them from the driver), `within`/`has` raise `ValueError` instead of
silently dropping them; set those options on the outer locator instead. On
the vision path (no accessibility tree, or `strategy="vision"`), a plain
`text` locator is an OCR match, but a
locator with `query`, `within`, `has`, or `nth` is resolved by one
vision-model call instead, with a prompt built from the whole locator;
`nth` works the same way on a `query` locator as on a plain one.

### Accessibility mode

With accessibility mode on, the phone exposes its accessibility tree and
locators resolve against it: exact roles, names and ids instead of pixels.
Accessibility mode is off by default, so `client.session(...)` allocates any
phone. Pass `accessibility=True` to turn it on; it needs a phone that
supports it, and `client.session(...)` then only claims such phones.

```python
with client.session("android", accessibility=True) as driver:
    driver.get_by_role("button", name="Log in").tap()
    driver.get_by_role("checkbox", name="Remember me", states=["checked"]).wait_for()
    driver.locator(role="textbox", package_name="com.example.app").fill("me@example.com")
    driver.get_by_id("com.example.app:id/submit").wait_for(state="enabled")
    driver.locator(query="the log in button", strategy="vision").tap()  # skip the tree
```

- With `accessibility=True`, a `phone_id` that can't run it raises
  `AccessibilityUnavailableError` (an `ApiError` subclass), and a pool with
  no free capable phone is the usual no-phone 409. Without it (the default,
  `accessibility=False`), any phone is allocated with the tree off.
  `driver.accessibility.enabled_at_allocation` is the allocated value.
- **What apps can see:** while it is on, the accessibility service is
  enabled and any app on the phone can see that, and some apps change
  behavior or flag the session. Off means fully off: no service is enabled.
- The tree-only selectors (`role`, `name`, `id`, `states`, `value`,
  `window_id`, `node_id`, `android_class_name`, `package_name`, and
  `wait_for(state="enabled")`) raise `StrategyUnavailableError` on a
  session without a tree, under every `strategy`; they are never turned
  into a model prompt. `strategy` is `"auto"` (tree when there is one),
  `"vision"`, or `"accessibility"`.

`driver.accessibility` reads the raw tree and toggles it mid-session:

```python
tree = driver.accessibility.snapshot()            # AXTree: nodes, windows, captured_at
buttons = driver.accessibility.query(role="button", name="Log in")
driver.locator(node_id=buttons[0].node_id).tap()  # exactly that node
driver.accessibility.children(tree.windows[0].root_id)
driver.accessibility.state()                      # AccessibilityState(enabled, toggleable)
driver.accessibility.disable()                    # returns once the phone confirms
driver.accessibility.enable()
```

`snapshot(interesting_only=True, window_id=None, depth=None)`,
`query(role=None, name=None, selector=None)`, `partial(node_id,
fetch_relatives=True)` and `children(node_id)` raise
`StrategyUnavailableError` while the tree is off, `TreeUnavailableError`
when there's no app window to read (a system dialog is up), and
`StaleNodeError` for a node that's gone. On a session that doesn't offer
the tree at all, they raise `UnknownOpError`.

### Screen snapshots

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

On Windows, in PowerShell (use `setx AXILIO_API_KEY axl_...` to keep it for
new terminals, or `set AXILIO_API_KEY=axl_...` in cmd):

```powershell
$env:AXILIO_API_KEY = "axl_..."
```

The SDK is pure Python and supports Linux, macOS and Windows. CI runs the test
suite on Linux and Windows.

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
| `client.argus` | Vision inference (argus 2.0) | `models.list_models()`, `screenshots.detect()`, `screenshots.locate()`, `accessibility_trees.accessibility_trees_locate()` |
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

**Argus** calls (`client.argus`) raise argus's own generated errors, all
subclasses of `axilio.argus.core.api_error.ApiError`, with the RFC 9457
problem body parsed into `e.body` (`title`, `status`, `detail`, `code`);
for example `axilio.argus.errors.PaymentRequiredError` on a 402.

**Device-control** calls raise typed exceptions from `axilio.drivers.mobile`,
all of which subclass its `AxilioError`:

```python
from axilio.drivers.mobile import ActionTimeoutError

with client.session("android") as driver:
    try:
        driver.locator(query="a button that isn't there").tap(timeout=5)
    except ActionTimeoutError:
        ...  # never became actionable within the budget (also a builtin TimeoutError)
```

Others include `ConnectionError`, `DeviceOfflineError`, `NotConnectedError`,
`InvalidArgsError`, `UnauthorizedError`, and, for accessibility mode,
`StrategyUnavailableError`, `TreeUnavailableError` and `StaleNodeError`.

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
