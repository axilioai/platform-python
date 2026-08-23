# Changelog

Release notes for the Axilio Python SDK. Versions are git tags (`vX.Y.Z`);
entries here call out anything a release changes that upgrading code must
know about — most importantly breaking changes.

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
