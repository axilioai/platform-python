#!/usr/bin/env python3
"""AXI-1982 live + capture/replay validation for the installed Python SDK.

The live leg is read-only against dev/staging. The future-kind leg runs only
against a loopback HTTP server, so this probe never injects synthetic telemetry
into a deployment. Results contain types/counts and never API keys or frame
bodies/attributes.
"""

from __future__ import annotations

import argparse
import asyncio
import importlib.metadata
import json
import os
import sys
import threading
import time
import urllib.parse
from collections.abc import Callable
from dataclasses import asdict, dataclass
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any

import pydantic

from axilio import AsyncAxilioApi
from axilio.core import ParsingError
from axilio.platform import Client
from axilio.types.run_session_frames_response_frames_item import (
    RunSessionFramesResponseFramesItem_Log,
    RunSessionFramesResponseFramesItem_Span,
    RunSessionFramesResponseFramesItem_Unknown,
)


@dataclass
class Result:
    id: str
    status: str
    classification: str
    started_at: str
    duration_ms: int
    attempts: int
    expected: str
    observed_redacted: str


class Recorder:
    def __init__(self) -> None:
        self.results: list[Result] = []

    def check(self, test_id: str, expected: str, fn: Callable[[], str]) -> None:
        started = time.time()
        started_at = _rfc3339(started)
        try:
            observed = fn()
            status = "PASS"
            classification = "PASS"
        except Exception as exc:  # noqa: BLE001 - every check must become evidence
            observed = f"{type(exc).__name__}: {exc}"
            status = "FAIL"
            classification = "SDK_ARTIFACT_FAILURE"
        self.results.append(
            Result(
                id=test_id,
                status=status,
                classification=classification,
                started_at=started_at,
                duration_ms=int((time.time() - started) * 1000),
                attempts=1,
                expected=expected,
                observed_redacted=observed,
            )
        )

    @property
    def passed(self) -> bool:
        return all(result.status == "PASS" for result in self.results)


def _rfc3339(timestamp: float) -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(timestamp))


def _assert(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def _validate_target(environment: str, base_url: str) -> str:
    if environment not in {"dev", "staging"}:
        raise ValueError("environment must be dev or staging; production is refused")
    parsed = urllib.parse.urlsplit(base_url.rstrip("/"))
    if parsed.hostname == "api.axilio.ai":
        raise ValueError("production origin is refused")
    if parsed.username or parsed.password or parsed.query or parsed.fragment:
        raise ValueError("base URL must not contain credentials, query, or fragment")
    if parsed.path not in {"", "/"}:
        raise ValueError("base URL must be an origin without /api/v1")
    if environment == "staging" and base_url.rstrip("/") != "https://staging-api.axilio.ai":
        raise ValueError("staging must use exactly https://staging-api.axilio.ai")
    loopback = parsed.hostname in {"127.0.0.1", "localhost", "::1"}
    if parsed.scheme != "https" and not (
        environment == "dev" and parsed.scheme == "http" and loopback
    ):
        raise ValueError("HTTPS is required; only loopback dev may use HTTP")
    return base_url.rstrip("/")


def _load_manifest(path: Path, environment: str) -> dict[str, Any]:
    manifest = json.loads(path.read_text(encoding="utf-8"))
    _assert(manifest.get("manifest_version") == 1, "manifest_version must be 1")
    _assert(manifest.get("environment") == environment, "manifest environment mismatch")
    _assert(
        manifest.get("seed_revision") not in {None, "", "unknown"}, "manifest provenance missing"
    )
    fixtures = manifest.get("fixtures")
    _assert(isinstance(fixtures, dict), "fixtures object missing")
    for name in ("normal_session", "normal_empty_session", "expired_session"):
        fixture = fixtures.get(name)
        _assert(isinstance(fixture, dict) and bool(fixture.get("id")), f"{name} fixture missing")
    return manifest


def _package_version() -> str:
    return importlib.metadata.version("axilio")


def run_live(
    environment: str, base_url: str, api_key: str, manifest: dict[str, Any], recorder: Recorder
) -> None:
    fixtures = manifest["fixtures"]
    client = Client(api_key=api_key, base_url=base_url, timeout=10.0, max_retries=0)

    def raw_normal() -> str:
        page = client.raw.runs.sessions_list_frames(
            fixtures["normal_session"]["id"], limit=100, offset=0
        )
        _assert(page.retention_expired is False, "normal page marked retention-expired")
        _assert(
            len(page.frames or []) >= fixtures["normal_session"].get("min_frames", 1),
            "normal frames missing",
        )
        _assert(isinstance(page.sdk_call_costs, dict), "normal sdk_call_costs is not dict")
        _assert(isinstance(page.inference_costs, dict), "normal inference_costs is not dict")
        _assert(
            all(
                isinstance(
                    frame,
                    RunSessionFramesResponseFramesItem_Span
                    | RunSessionFramesResponseFramesItem_Log,
                )
                for frame in page.frames or []
            ),
            "today's backend returned a non-span/log frame",
        )
        return f"frames={len(page.frames or [])} maps=dict"

    recorder.check(
        "PY-01", "raw normal page parses as known frames with dictionary maps", raw_normal
    )

    def raw_expired_sync() -> str:
        page = client.raw.runs.sessions_list_frames(
            fixtures["expired_session"]["id"], limit=7, offset=3
        )
        _assert(page.retention_expired is True, "expired flag false")
        _assert(page.frames == [], "expired frames not empty")
        _assert(
            page.sdk_call_costs is None and page.inference_costs is None,
            "raw null maps did not become None",
        )
        _assert(page.limit == 7 and page.offset == 3, "expired pagination not preserved")
        return "retention=true frames=[] maps=None pagination=7/3"

    recorder.check(
        "PY-02-SYNC",
        "raw sync expired page exposes None maps without ParsingError",
        raw_expired_sync,
    )

    async def raw_expired_async() -> str:
        async_client = AsyncAxilioApi(
            api_key=api_key, base_url=f"{base_url}/api/v1", timeout=10.0, max_retries=0
        )
        page = await async_client.runs.sessions_list_frames(
            fixtures["expired_session"]["id"], limit=7, offset=3
        )
        _assert(page.retention_expired is True, "async expired flag false")
        _assert(page.frames == [], "async expired frames not empty")
        _assert(
            page.sdk_call_costs is None and page.inference_costs is None,
            "async null maps did not become None",
        )
        return "retention=true frames=[] maps=None"

    recorder.check(
        "PY-02-ASYNC",
        "raw async expired page exposes None maps without ParsingError",
        lambda: asyncio.run(raw_expired_async()),
    )

    def high_expired() -> str:
        trace = client.telemetry(fixtures["expired_session"]["id"]).trace()
        _assert(trace.retention_expired is True, "trace retention flag false")
        _assert(
            not trace.spans and not trace.logs and not trace.unknown, "expired trace has frames"
        )
        _assert(
            trace.sdk_call_costs == {} and trace.inference_costs == {},
            "high-level maps are not empty dicts",
        )
        return "retention=true spans=0 logs=0 unknown=0 maps={}"

    recorder.check(
        "PY-03", "high-level expired trace normalizes null maps to empty dictionaries", high_expired
    )

    def high_normal() -> str:
        trace = client.telemetry(fixtures["normal_session"]["id"]).trace()
        _assert(not trace.retention_expired, "normal trace marked expired")
        _assert(
            len(trace.spans) + len(trace.logs) >= fixtures["normal_session"].get("min_frames", 1),
            "known frames lost",
        )
        _assert(trace.unknown == [], "today's backend returned unknown frames")
        _assert(
            isinstance(trace.sdk_call_costs, dict) and isinstance(trace.inference_costs, dict),
            "trace maps not dict",
        )
        return f"spans={len(trace.spans)} logs={len(trace.logs)} unknown=0"

    recorder.check("PY-04", "high-level normal trace keeps every known frame", high_normal)

    def summaries() -> str:
        expired_id = fixtures["expired_session"]["id"]
        normal_id = fixtures["normal_session"]["id"]
        expired_summary = client.telemetry(expired_id).summary()
        expired_logs = list(client.telemetry(expired_id).logs())
        normal_summary = client.telemetry(normal_id).summary()
        normal_logs = list(client.telemetry(normal_id).logs())
        _assert(expired_logs == [], "expired logs not empty")
        return (
            f"expired_summary={type(expired_summary).__name__} "
            f"normal_summary={type(normal_summary).__name__} "
            f"normal_logs={len(normal_logs)}"
        )

    recorder.check(
        "PY-05", "summary/log helpers remain safe for normal and expired traces", summaries
    )

    def provenance() -> str:
        version = _package_version()
        _assert(version == "0.20.0", f"installed axilio version is {version}, want 0.20.0")
        imported = Path(sys.modules["axilio"].__file__ or "").resolve()
        _assert(
            "site-packages" in str(imported) or "dist-packages" in str(imported),
            f"axilio imported from workspace path {imported}",
        )
        return f"axilio={version} pydantic={pydantic.__version__} import=isolated"

    recorder.check(
        "PY-06", "candidate package provenance and Pydantic runtime are explicit", provenance
    )


def _span(**updates: Any) -> dict[str, Any]:
    value: dict[str, Any] = {
        "kind": "span",
        "phase": "end",
        "span_type": "sdk_call",
        "trace_id": "0" * 32,
        "span_id": "1" * 16,
        "name": "Screen.observe",
        "start_time_unix_nano": 1,
        "end_time_unix_nano": 2,
        "status": {"code": "ok", "message": ""},
        "attributes": {},
    }
    value.update(updates)
    return value


def _log(index: int = 0, **updates: Any) -> dict[str, Any]:
    value: dict[str, Any] = {
        "kind": "log",
        "log_type": "output_log",
        "trace_id": "0" * 32,
        "span_id": "1" * 16,
        "time_unix_nano": 10 + index,
        "severity": "INFO",
        "body": "synthetic",
        "attributes": {},
    }
    value.update(updates)
    return value


METRIC = {
    "kind": "metric",
    "name": "axi.e2e.synthetic",
    "value": 0.72,
    "nested": {"unit": "ratio"},
    "tags": ["a", "b"],
}


def _response(
    frames: list[dict[str, Any]],
    *,
    total: int | None = None,
    limit: int = 100,
    offset: int = 0,
    retention: bool = False,
    null_maps: bool = False,
) -> dict[str, Any]:
    maps: dict[str, int] | None = None if null_maps else {}
    return {
        "frames": frames,
        "total": len(frames) if total is None else total,
        "limit": limit,
        "offset": offset,
        "retention_expired": retention,
        "sdk_call_costs": maps,
        "inference_costs": maps,
    }


class ReplayHandler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def log_message(self, _format: str, *_args: Any) -> None:
        return

    def do_GET(self) -> None:  # noqa: N802 - BaseHTTPRequestHandler API
        parsed = urllib.parse.urlsplit(self.path)
        session_id = parsed.path.removeprefix("/api/v1/phones/sessions/").removesuffix("/frames")
        query = urllib.parse.parse_qs(parsed.query)
        offset = int(query.get("offset", ["0"])[0])
        limit = int(query.get("limit", ["100"])[0])
        status = 200
        if session_id == "mixed":
            payload = _response([_span(), METRIC, _log()])
        elif session_id == "extra-known":
            payload = _response(
                [_span(span_type="future_role", future_field={"x": 1}), _log(log_type="future_log")]
            )
        elif session_id == "malformed-span":
            payload = _response([{"kind": "span", "phase": "end"}])
        elif session_id == "malformed-log":
            payload = _response([{"kind": "log", "body": "synthetic"}])
        elif session_id.startswith("bad-kind-"):
            bad: Any = {
                "missing": None,
                "empty": "",
                "null": None,
                "number": 7,
                "object": {"x": 1},
                "array": ["metric"],
            }[session_id.removeprefix("bad-kind-")]
            frame = {} if session_id.endswith("missing") else {"kind": bad}
            payload = _response([frame])
        elif session_id == "expired":
            payload = _response(
                [], total=0, limit=limit, offset=offset, retention=True, null_maps=True
            )
        elif session_id == "paged":
            if offset == 0:
                payload = _response(
                    [_log(i) for i in range(1000)], total=1001, limit=1000, offset=0
                )
                payload["sdk_call_costs"] = {"1" * 16: 12}
            elif offset == 1000:
                payload = _response([METRIC], total=1001, limit=1000, offset=1000, null_maps=True)
            else:
                status = 500
                payload = {"error": "unexpected third page"}
        else:
            status = 404
            payload = {"error": "not found"}
        body = json.dumps(payload, separators=(",", ":")).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Connection", "close")
        self.end_headers()
        self.wfile.write(body)


class ReplayServer:
    def __enter__(self) -> str:
        self.server = ThreadingHTTPServer(("127.0.0.1", 0), ReplayHandler)
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        return f"http://127.0.0.1:{self.server.server_port}"

    def __exit__(self, *_args: Any) -> None:
        self.server.shutdown()
        self.server.server_close()
        self.thread.join(timeout=5)


def run_replay(recorder: Recorder) -> None:
    with ReplayServer() as base_url:
        client = Client(api_key="axl_loopback", base_url=base_url, timeout=5.0, max_retries=0)

        def mixed() -> str:
            page = client.raw.runs.sessions_list_frames("mixed")
            frames = page.frames or []
            _assert(len(frames) == 3, "mixed page count changed")
            _assert(
                isinstance(frames[0], RunSessionFramesResponseFramesItem_Span), "span not typed"
            )
            _assert(
                isinstance(frames[1], RunSessionFramesResponseFramesItem_Unknown),
                "metric not unknown",
            )
            _assert(isinstance(frames[2], RunSessionFramesResponseFramesItem_Log), "log not typed")
            _assert(frames[1].raw == METRIC, f"unknown raw mismatch: {frames[1].raw}")
            trace = client.telemetry("mixed").trace()
            _assert(
                len(trace.spans) == 1 and len(trace.logs) == 1 and len(trace.unknown) == 1,
                "high-level siblings lost",
            )
            _assert(trace.unknown[0].raw == METRIC, "public unknown raw mismatch")
            return "raw=span,unknown,log high=1/1/1 semantic-roundtrip=true"

        recorder.check("REPLAY-01", "future metric survives between typed known siblings", mixed)

        def extra_known() -> str:
            page = client.raw.runs.sessions_list_frames("extra-known")
            frames = page.frames or []
            _assert(len(frames) == 2, "extra-known frame count")
            _assert(
                isinstance(frames[0], RunSessionFramesResponseFramesItem_Span),
                "new span role became unknown",
            )
            _assert(
                isinstance(frames[1], RunSessionFramesResponseFramesItem_Log),
                "new log role became unknown",
            )
            _assert(
                frames[0].span_type == "future_role" and frames[1].log_type == "future_log",
                "new role strings lost",
            )
            return "known models retained future role strings"

        recorder.check(
            "REPLAY-02", "new fields/role strings remain additive inside known kinds", extra_known
        )

        def malformed_known() -> str:
            for session_id in ("malformed-span", "malformed-log"):
                try:
                    client.raw.runs.sessions_list_frames(session_id)
                except ParsingError:
                    continue
                raise AssertionError(f"{session_id} fell through to Unknown")
            return "span+log ParsingError"

        recorder.check(
            "REPLAY-03", "malformed known frame fails instead of becoming unknown", malformed_known
        )

        def malformed_kinds() -> str:
            for name in ("missing", "empty", "null", "number", "object", "array"):
                try:
                    client.raw.runs.sessions_list_frames(f"bad-kind-{name}")
                except ParsingError:
                    continue
                raise AssertionError(f"bad kind {name} parsed successfully")
            return "missing,empty,null,number,object,array rejected"

        recorder.check(
            "REPLAY-04", "only non-empty unknown strings enter the fallback", malformed_kinds
        )

        def expired() -> str:
            page = client.raw.runs.sessions_list_frames("expired", limit=7, offset=3)
            trace = client.telemetry("expired").trace()
            _assert(
                page.sdk_call_costs is None and page.inference_costs is None,
                "raw replay maps not None",
            )
            _assert(
                trace.sdk_call_costs == {} and trace.inference_costs == {},
                "high replay maps not dict",
            )
            return "raw=None high={}"

        recorder.check(
            "REPLAY-05", "replayed expired body preserves raw/high-level map semantics", expired
        )

        def paged() -> str:
            trace = client.telemetry("paged").trace()
            _assert(len(trace.logs) == 1000, f"logs={len(trace.logs)}")
            _assert(
                len(trace.unknown) == 1 and trace.unknown[0].raw == METRIC, "page-two unknown lost"
            )
            _assert(trace.sdk_call_costs == {"1" * 16: 12}, "page-one costs lost")
            return "items=1001 pages=2 logs=1000 unknown=1 costs-preserved"

        recorder.check(
            "REPLAY-06", "two-page aggregation keeps 1001 items and page-one costs", paged
        )
        recorder.check(
            "REPLAY-07", "unknown decode/public conversion preserves semantic JSON", mixed
        )

        async def async_mixed() -> str:
            async_client = AsyncAxilioApi(
                api_key="axl_loopback", base_url=f"{base_url}/api/v1", timeout=5.0, max_retries=0
            )
            page = await async_client.runs.sessions_list_frames("mixed")
            frames = page.frames or []
            _assert(
                len(frames) == 3
                and isinstance(frames[1], RunSessionFramesResponseFramesItem_Unknown),
                "async unknown missing",
            )
            return "sync+async classification=span,unknown,log"

        recorder.check(
            "REPLAY-08",
            "sync and async generated clients classify mixed page identically",
            lambda: asyncio.run(async_mixed()),
        )


def write_results(
    path: Path,
    recorder: Recorder,
    *,
    environment: str,
    sdk_ref: str,
    artifact_sha256: str,
) -> None:
    payload = {
        "environment": environment,
        "sdk": "python",
        "sdk_ref": sdk_ref,
        "package_version": _package_version(),
        "artifact_sha256": artifact_sha256,
        "pydantic_version": pydantic.__version__,
        "verdict": "PASS" if recorder.passed else "SDK_ARTIFACT_FAILURE",
        "results": [asdict(result) for result in recorder.results],
    }
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--env", choices=("dev", "staging"), required=True)
    parser.add_argument("--base-url", required=True)
    parser.add_argument("--fixture-manifest", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--sdk-ref", required=True)
    parser.add_argument("--artifact-sha256", required=True)
    parser.add_argument("--replay-only", action="store_true")
    args = parser.parse_args()

    recorder = Recorder()
    base_url = _validate_target(args.env, args.base_url)
    manifest = _load_manifest(args.fixture_manifest, args.env)
    api_key = os.environ.get("AXILIO_API_KEY", "")
    if not args.replay_only:
        if not api_key:
            raise SystemExit("AXILIO_API_KEY is required for live validation")
        run_live(args.env, base_url, api_key, manifest, recorder)
    run_replay(recorder)
    write_results(
        args.output,
        recorder,
        environment=args.env,
        sdk_ref=args.sdk_ref,
        artifact_sha256=args.artifact_sha256,
    )
    if recorder.passed:
        print(f"AXI-1982 Python validation PASS ({pydantic.__version__}); evidence {args.output}")
        return 0
    print(
        f"AXI-1982 Python validation SDK_ARTIFACT_FAILURE; evidence {args.output}", file=sys.stderr
    )
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
