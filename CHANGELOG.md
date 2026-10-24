# Changelog

Release notes for the Axilio Python SDK. Versions are git tags (`vX.Y.Z`);
entries here call out anything a release changes that upgrading code must
know about — most importantly breaking changes.

## v0.22.0

Session telemetry over Server-Sent Events (AXI-2975), and the client
regenerated from the production API at 0.150.0, which renamed several
operations (AXI-1764). Needs the production API at 0.150.0 or later.

- **Breaking (transport):** `TelemetryTail` reads the session's event stream
  (`GET /api/v1/realtime/sessions/{session_id}/events`) instead of the retired
  `/ws/telemetry` WebSocket. A fresh tail starts with the trace so far, then
  follows live; the server deduplicates, and a dropped stream resumes with
  `Last-Event-ID` and no gap. The tail ends when the session does (its end
  frame, or a 204 once nothing is left), and works on an ended session too.
- **Breaking:** a refused stream raises `UnauthorizedError` (401/403), the new
  `SessionNotFoundError` (404) or the new `TelemetryOffError` (409).
  `SessionEndedError` is no longer raised by the tail: the end of a session
  just ends the loop. `TelemetryTail` takes `headers=` and drops `connect`'s
  WebSocket signature.
- `client.telemetry(session_id).tail()` no longer needs `telemetry_url`: without
  it, the tail opens the session's stream on the API host with the client's
  API key, so a run's session can be followed by id.
- **Breaking (removed):** `client.phones.session_telemetry_token(...)`. The API
  no longer mints telemetry tokens; follow a session with
  `client.telemetry(session_id).tail()` instead.
- **Breaking (renamed):** these methods follow the API's new operation names:

  | Before | Now |
  |---|---|
  | `client.argus.detect(...)` | `client.argus.screenshots.detect(...)` |
  | `client.argus.locate(...)` | `client.argus.screenshots.locate(...)` |
  | `client.argus.list_models()` | `client.argus.models.list()` |
  | `client.files.rename(...)` | `client.files.update(...)` |
  | `client.phones.nickname(...)` | `client.phones.update(...)` |
  | `client.runs.stats(workflow_id)` | `client.workflows.get_run_stats(workflow_id)` |
  | `client.workflows.save_code(...)` | `client.workflows.create_revision(...)` |

- **Breaking (removed):** `client.phones.active_sessions(...)` (use
  `client.phones.list_sessions(status=...)`) and
  `client.phones.session_thumbnail(...)`.
- New: `client.argus.elements.locate(...)` picks one of the elements you pass
  in by description; `client.files.get(...)`;
  `client.phones.stream_session_events(...)`; `client.messages` and
  `client.conversations` for a phone's SMS and MMS;
  `client.billing.get_balance_statement(...)` and
  `client.billing.list_balance_transactions(...)`.
- Argus errors are RFC 9457 problem+json: each status raises its own generated
  error (`BadRequestError`, `UnauthorizedError`, `PaymentRequiredError`,
  `UnprocessableEntityError`, `InternalServerError`, `BadGatewayError` in
  `axilio.argus.errors`) with the body parsed into `Problem` (`title`,
  `status`, `detail`, `code`). `HTTPValidationError` / `ValidationError`
  are removed.

### Accessibility mode (AXI-2116)

Locators can resolve against the phone's accessibility tree (exact roles,
names and resource ids) instead of the screen. Without a tree, the tree-only
locators raise `StrategyUnavailableError`.

- `client.session(..., accessibility: bool = False)` is always sent to
  allocate. Accessibility mode is off by default (AXI-2230), so a session
  gets any phone. Pass `accessibility=True` to turn it on; it needs a phone
  that supports it (only such phones are claimed). The allocated value is
  `driver.accessibility.enabled_at_allocation`. `client.workflows.create`
  takes `accessibility` too (default false) and `update` takes it as an
  optional change; the allocate response, session detail and workflow
  summary return it.
- What apps can see: while accessibility mode is on, the accessibility
  service is enabled and any app on the phone can see it. Off means fully
  off.
- New: `AccessibilityUnavailableError` (an `ApiError`, HTTP 409) when
  `accessibility=True` names a `phone_id` that can't run it, raised from
  both `client.session(...)` and `client.phones.allocate(...)`. An exhausted
  pool stays the ordinary no-phone 409. `SessionEndReason` types the
  session.ended `end_reason`, including the new `accessibility_unavailable`
  (the phone couldn't confirm the state before handover).
- Public now: `get_by_role(role, name=, exact=, states=)`, `get_by_id(id)`,
  and on `locator(...)` the `role` / `name` / `id` / `states` /
  `android_class_name` fields plus the new `value`, `window_id`, `node_id`
  and `package_name` (wire `platform.android.packageName`). Every locator
  constructor takes `strategy=` (`"auto"` / `"vision"` / `"accessibility"`,
  the `Strategy` type), with `default_strategy` on the driver and on
  `client.session(...)`. `wait_for(state="enabled")` is in `WaitState`.
  Tree-only selectors raise `StrategyUnavailableError` without a tree under
  every strategy; they're never turned into a model prompt.
- New: `driver.accessibility` with `snapshot(interesting_only=True,
  window_id=None, depth=None) -> AXTree`, `query(role=, name=, selector=)`,
  `partial(node_id, fetch_relatives=True)`, `children(node_id)`, `state()`,
  `enable()` and `disable()` (the toggle carries an idempotency key like
  the other mutating calls). Types: `AXTree`, `AXNode`, `AXWindow`,
  `AXValue`, `AXProperty`, `AXAndroidNode`, `AccessibilityState`.
- New exceptions: `TreeUnavailableError` (the tree is on but has no app
  window, e.g. a permission dialog is up) and `StaleNodeError` (a `node_id`
  that's gone).

## v0.21.0

Scheduled runs and webhooks (AXI-2098), from the production API.

- New: `client.runs.create(..., start_at=...)` books runs for a set time, 60
  seconds to 30 days ahead. They are listed with status `scheduled` until then,
  start within about 15 seconds of that time, and can be cancelled with
  `client.runs.cancel(run_id)` until they start. For a scheduled run,
  `start_timeout_seconds` counts from its start time, not from booking.
  `RunResponse.start_at` holds the booked time.
- New: `client.webhooks`, for webhook endpoints (create, list, get, delete,
  rotate the signing secret, send a test event), their deliveries (list, get,
  attempts, replay), delivery metrics, and the list of event types.
- Phone status can also be `recovering` or `out_of_service`, and run status
  `scheduled`.
- **Breaking:** the file-delete response drops `phones_pending_removal`. It was
  deprecated and always 0, since a library delete no longer removes copies from
  phones.
- **Behaviour change:** the client no longer resends a POST or PATCH after a
  5xx. The API takes no idempotency keys, so a create that took effect but
  answered 500 used to run twice (two webhook endpoints, the first one's
  signing secret lost; or every run booked twice). Such a call now raises
  `ApiError`; check whether it took effect before calling again. 429 and 408
  are still retried for every method, and a 5xx for GET, PUT and DELETE. A 409
  is no longer retried. The same goes for a dropped connection: a POST or PATCH
  whose connection closed before the response arrived raises
  `httpx.RemoteProtocolError` instead of being sent again. A connection that
  never opened (`httpx.ConnectError`) is still retried for every method.
- `repr()` and `str()` of a response print `[redacted]` for one-time secrets:
  webhook signing secrets, API key values, sign-in tokens, and the session's
  `live_view_url`, `control_url` and `telemetry_url`, which each carry a token.
  The attributes and `model_dump()` still return them.
- The lockfile moves to anyio 4.14.2, for two advisories in earlier versions
  (TLS host name encoding, and process-pool workers blocking on stderr).

## v0.20.2

- Adds the `aiohttp` extra (AXI-2227). `pip install axilio[aiohttp]` installs
  `httpx-aiohttp`, which the async clients pick up to run on aiohttp. The
  generated argus client's error message used to suggest
  `pip install axilio.argus[aiohttp]`, which isn't a real package; it now
  names `axilio[aiohttp]`, and a regen step keeps it that way.

## v0.20.1

- Ctrl+C now interrupts a mobile-driver call that is waiting on the phone,
  on Windows too (AXI-2226). On Windows a blocking socket read never returned
  for Ctrl+C, so a stalled `observe()`, `screenshot()` or input call (or a
  Jupyter cell running one) could only be stopped by killing the process.
  Calls now wait in short slices, and an interrupted call drops its
  connection; the next call reconnects.
- A timed call now returns at its deadline even when the reply trickles in a
  few bytes at a time (each socket read is bounded by the time left), and
  without the up-to-3 s close handshake that used to follow a timeout.
- A call without `timeout=` now waits for its reply with no deadline every
  time. Before, it inherited the 10 s connect timeout on a fresh connection
  and had no deadline after the first call that passed `timeout=`.
- A test factory passed as `MobileDriver.connect_remote(connect=...)` must now
  return connections with `abort()` (a close that skips the close handshake)
  as well as `send`, `recv`, `settimeout` and `close`. One without it is
  refused with `TypeError` on the first call, instead of leaking its socket on
  a timeout.

## v0.20.0

Adds the DCP Locator action tier (AXI-2105) and drops the client-side
selector loop it replaces. **Breaking:** the mobile driver's selector API.

- New: `driver.locator(...)` and `get_by_text(text, exact=False)` return a
  lazy, immutable `Locator`; nothing is sent until an action/query is
  called, so it always resolves against the current screen. Refine with
  `nth()`, `first()`, `within()`, `has()`, `filter(query=...)`; each keeps
  whatever options the locator it's called on was built with.
  `tap()` / `fill(text)` / `press(key)` / `wait_for(state=...)` /
  `bounding_box()` / `text()` / `count()` take only `timeout=` and resolve,
  auto-wait, and (for tap/fill/press) act in one round trip, returning a
  `LocatorResult` (`resolved_by`, `bounds`, `took_ms`, `model_name`).
  `driver.press(key)` presses the focused element without a locator, and
  takes no resolution options at all.
- `model=` and `ocr_engine=` live on the locator constructors (`locator(...)`,
  `get_by_text(...)`), not on the action/query methods: the locator is what
  resolves the target, so it's what picks how. Precedence: a locator's own
  value, else the driver default (`default_model` / `default_ocr_engine` on
  `connect(...)` / `connect_remote(...)` / `client.session(...)`), else
  omitted from the wire. `within(other)` / `has(other)` take only `other`'s
  selector fields into the scope; the outer locator's options govern the
  whole call, since the edge resolves the whole locator, scopes included, in
  one call. If `other` itself sets `model` or `ocr_engine` (not just an
  inherited driver default), `within`/`has` raise `ValueError` at build time
  instead of silently dropping them.
- Edge behavior on the vision path: a plain `text` locator is still an OCR
  match, but any locator carrying `query`, `within`, `has`, or `nth` is now
  resolved by one vision-model call, with a prompt composed from the whole
  locator. `nth` works on a `query` locator the same as on a plain one (it
  no longer needs to be `0`). `count()` needs a plain text locator; one that
  also carries `query`, `within`, or `has` raises `InvalidArgsError`.
- New exception: `ActionTimeoutError` (also catchable as the builtin
  `TimeoutError`), raised when a locator's auto-wait times out.
  `StrategyUnavailableError` is also new, mapping the DCP kind a resolver
  that needs the accessibility tree returns; nothing in today's public
  surface can trigger it (see below), but a raw DCP caller can still see it.
- Not yet public: `get_by_role(role, name=...)`, `get_by_id(id)`, the
  `role` / `name` / `id` / `states` / `android_class_name` parameters on
  `locator(...)`, the `strategy=` option, and the `Strategy` type all need
  an accessibility tree, which no phone exposes yet. They're held back from
  this release rather than shipped as dead weight, and will land together
  with accessibility support in a later release. `wait_for(state=...)`
  accepts only `"visible"` and `"hidden"` for the same reason (there's no
  `"enabled"` signal without a tree either).
- Removed: `ElementNotFoundError`. The DCP `Screen.find` method and the
  `ElementNotFound` kind are retired from the wire; a locator that matches
  nothing raises `ActionTimeoutError`, and `locator(query=...)` replaces
  `find(query=...)`.
- Removed: `MobileDriver.find()`, `find_text()`, `find_all_text()`,
  `wait_for_text()`, `wait_until_gone()`, and the predicate `wait_for()`.
  Each was a client-side poll loop or a single-shot call that froze a stale
  center; the Locator tier replaces all of them server-side, auto-waiting
  in the same round trip as the action.
- `Element` is plain data now (`bbox`, `center`, `confidence`, `text`,
  `source`). It lost `tap()` / `long_press()` / `type_into()` /
  `swipe_to()` and its driver back-reference. `observe()` and `Screen`
  (`find_text` / `find_all_text` as pure data filters over one already-
  captured frame) are unchanged; resolve a `Locator` instead of acting on
  an `Element`.

## v0.19.0

Regenerated against backend spec 0.83.0 (AXI-1905). **Breaking:** the file API
unified `/uploads` + `/downloads` into one `/files` collection.

- `client.uploads` and `client.downloads` are removed; use `client.files`
  (`list`, `create`, `complete`, `delete`, `rename`, `phones_session_files`).
- `FileSummary` gains `source` (`upload` | `capture`) and, for captures,
  `surface`, `session_id`, `capture_state`, `capture_error`, `checksum`.
  `DownloadSummary` / `DownloadListResponse` are gone — a captured file is a
  `FileSummary` with `source == "capture"`.
- `client.files.list(...)` takes the filters `q`, `mime_type`, size and date
  bounds, `source`, `surface`, `session_id`.
- The hand-written `client.files` helpers (`upload`/`push`/`send`/`list`/
  `delete`) are unchanged in signature; they now call the generated `files`
  client under the hood. `delete`'s parameter is `file_id` (was `upload_id`).

## v0.18.0

Regenerated against backend spec 0.82.0 (AXI-1859). No breaking changes.

New generated surfaces (the 2026-08-22 dashboard-parity promotions):

- `client.usage.list_sessions(...)` — per-session usage/cost listing.
- `client.phones.availability(...)` — consolidated capacity summary
  (shared pool by type/location + the caller's dedicated idle counts).
- `client.phones.session_live_view_token(...)` — re-mint a live-view
  (video) link for an active session.
- `client.phones.session_telemetry_token(...)` — mint telemetry-frames
  WebSocket access for an active session, so `client.telemetry(...)` can
  tail sessions the caller did not allocate.
- `client.billing.download_invoice(...)`, `update_auto_recharge(...)`,
  `update_usage_alerts(...)` — billing knobs (money movers stay in the
  dashboard).
- `client.organization.get()` / `list_members()` / `list_invitations()` —
  read-only org descriptor and listings.

Fixes:

- Span frames now mark `end_time_unix_nano` and `status` as optional,
  matching the live wire's start-phase frames (spec 0.82.0); the generated
  parser no longer rejects them. `axilio.platform.parse_frame` still
  canonicalizes absence to the in-flight sentinels (end `0`, status code
  `""`).
- Includes the telemetry live tail from AXI-1853 (`client.telemetry(...)`
  with `trace()` / `summary()` / `logs()`), whose stacked PR (#44) had
  merged into its base branch after that branch's own PR landed, so the
  module never reached `main` until this release.

## v0.17.0

Regenerated against backend spec 0.75.0; mobile driver gains transparent
reconnect with cursor resume and keyed re-send (AXI-1727).

### Breaking

- The telemetry listing endpoint moved: `GET
  /phones/sessions/{session_id}/events` is now `GET
  /phones/sessions/{session_id}/frames` (`sessions_list_frames`, spec
  0.75.0), returning the unified frame envelope. Production no longer
  serves the old `/events` path — it returns a plain 404, with no
  server-side alias. SDK releases generated before spec 0.75.0 therefore
  404 on telemetry listing and must upgrade to v0.17.0 or later. The break
  is deliberate: the platform is pre-GA with no external SDK users, so we
  break now rather than carry an alias (AXI-1850).
