# Changelog

Release notes for the Axilio Python SDK. Versions are git tags (`vX.Y.Z`);
entries here call out anything a release changes that upgrading code must
know about — most importantly breaking changes.

## v0.20.0

Regenerated against backend spec 0.86.0 (AXI-1982). The high-level telemetry
helper remains source-compatible; the raw generated response now truthfully
exposes the two cost maps as optional values.

- Retention-expired frame pages now accept raw `null` cost maps. The generated
  response exposes `None`; the high-level `trace()` helper keeps returning
  convenient empty dictionaries.
- The high-level `client.telemetry(...).trace()` reader preserves a future
  non-empty frame `kind` as `UnknownFrame` while keeping known siblings typed.
  Fern's generated low-level method remains strict on unknown kinds.
- Missing discriminators and malformed known span/log frames still fail on the
  archive path. The existing live `parse_frame()` fallback is unchanged.

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
