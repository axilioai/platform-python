# Changelog

Release notes for the Axilio Python SDK. Versions are git tags (`vX.Y.Z`);
entries here call out anything a release changes that upgrading code must
know about — most importantly breaking changes.

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
