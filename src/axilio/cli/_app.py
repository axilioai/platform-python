"""``axilio`` CLI implementation.

Stdlib ``argparse`` only, so ``pip install axilio`` gains the command with no extra
runtime dependency. Every command is a thin wrapper over the SDK: ``login`` persists
and verifies a key, ``session`` drives the phone-allocation lifecycle, and ``doctor``
sanity-checks the environment.
"""

from __future__ import annotations

import argparse
import getpass
import os
import sys

from .._config import load_api_key, load_config, save_config
from ..platform import ApiError, Client

_KEY_PREFIX = "axl_"


# --- entry point ----------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    handler = getattr(args, "handler", None)
    if handler is None:
        parser.print_help()
        return 2
    try:
        return handler(args)
    except KeyboardInterrupt:
        _err("aborted")
        return 130


# --- parser ---------------------------------------------------------------


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="axilio",
        description="Acquire and drive Axilio phones from the command line.",
    )
    sub = parser.add_subparsers(title="commands", metavar="<command>")

    p_login = sub.add_parser("login", help="Store and verify your API key.")
    p_login.add_argument("--api-key", help="axl_ key; you are prompted if this is omitted.")
    p_login.add_argument("--base-url", help="Override the API host (advanced).")
    p_login.set_defaults(handler=_cmd_login)

    p_doctor = sub.add_parser("doctor", help="Check your environment and credentials.")
    p_doctor.set_defaults(handler=_cmd_doctor)

    p_session = sub.add_parser("session", help="Acquire, list, and release phone sessions.")
    ssub = p_session.add_subparsers(title="session commands", metavar="<subcommand>")

    p_start = ssub.add_parser("start", help="Acquire a phone and open a session.")
    p_start.add_argument(
        "--phone-type", default="android", help="Phone type: android or ios (default android)."
    )
    p_start.add_argument("--phone-id", help="Pin a specific dedicated phone.")
    p_start.add_argument("--workflow-id", help="Attach the session to a workflow.")
    p_start.set_defaults(handler=_cmd_session_start)

    p_status = ssub.add_parser("status", help="List currently active sessions.")
    p_status.set_defaults(handler=_cmd_session_status)

    p_stop = ssub.add_parser("stop", help="Release a session by session id or phone id.")
    p_stop.add_argument("identifier", help="The session_id or phone_id to release.")
    p_stop.set_defaults(handler=_cmd_session_stop)

    p_session.set_defaults(handler=lambda _args, _p=p_session: (_p.print_help() or 2))

    return parser


# --- commands -------------------------------------------------------------


def _cmd_login(args: argparse.Namespace) -> int:
    key = args.api_key or getpass.getpass("Axilio API key (axl_...): ").strip()
    if not key:
        _err("no key provided.")
        return 1
    if not key.startswith(_KEY_PREFIX):
        _err(f"that does not look like an Axilio key (expected an {_KEY_PREFIX}... value).")
        return 1

    # Verify the key against the API before persisting it.
    try:
        balance = Client(api_key=key, base_url=args.base_url).billing.get_balance()
    except ApiError as e:
        if e.status_code in (401, 403):
            _err("that key was rejected (HTTP 401/403). Check it in the dashboard and retry.")
        else:
            _err(f"could not verify the key (HTTP {e.status_code}).")
        return 1
    except Exception as e:  # noqa: BLE001 — surface any transport/DNS error to the user
        _err(f"could not reach the API: {e}")
        return 1

    config = load_config()
    config["api_key"] = key
    if args.base_url:
        config["base_url"] = args.base_url
    path = save_config(config)
    print(f"Saved credentials to {path}.")
    print(f"Signed in. Balance: {balance.balance_display}.")
    return 0


def _cmd_doctor(_args: argparse.Namespace) -> int:
    ok = True

    py = sys.version_info
    py_ok = py >= (3, 10)
    _check(py_ok, f"Python {py.major}.{py.minor}.{py.micro}", "Axilio needs Python 3.10+")
    ok = ok and py_ok

    key = load_api_key() or os.environ.get("AXILIO_API_KEY")
    _check(bool(key), "API key found" if key else "no API key", "run `axilio login`")
    if not key:
        return 1

    try:
        client = Client()
        balance = client.billing.get_balance()
        _check(True, f"authenticated (balance {balance.balance_display})")
        print(f"    API host: {client.base_url}")
    except ApiError as e:
        _check(False, f"the API rejected the key (HTTP {e.status_code})", "re-run `axilio login`")
        ok = False
    except Exception as e:  # noqa: BLE001 — a CLI should report, not traceback
        _check(False, f"could not reach the API ({e})", "check your network / base URL")
        ok = False

    return 0 if ok else 1


def _cmd_session_start(args: argparse.Namespace) -> int:
    client = _client()
    kwargs: dict[str, str] = {"phone_type": args.phone_type.strip().upper()}
    if args.phone_id:
        kwargs["phone_id"] = args.phone_id
    if args.workflow_id:
        kwargs["workflow_id"] = args.workflow_id

    try:
        alloc = client.phones.allocate(**kwargs)
    except ApiError as e:
        _err(f"could not acquire a phone (HTTP {e.status_code}): {_detail(e)}")
        return 1

    print(f"session_id : {alloc.session_id}")
    print(f"phone_id   : {alloc.phone_id}")
    if alloc.region:
        print(f"region     : {alloc.region}")
    if alloc.live_view_url:
        print(f"live view  : {alloc.live_view_url}")
    if alloc.control_url:
        print(f"control_url: {alloc.control_url}")
    print()
    print(f"The phone stays leased until you run:  axilio session stop {alloc.session_id}")
    return 0


def _cmd_session_status(_args: argparse.Namespace) -> int:
    client = _client()
    try:
        resp = client.phones.active_sessions()
    except ApiError as e:
        _err(f"could not list sessions (HTTP {e.status_code}).")
        return 1

    sessions = resp.sessions or []
    if not sessions:
        print("No active sessions.")
        return 0

    print(f"{len(sessions)} active session(s):")
    for s in sessions:
        source = s.workflow_name or "interactive"
        phone = " ".join(x for x in (s.phone_type, s.model_name or s.phone_name) if x)
        print(f"  {s.session_id}  phone={s.phone_id}  {phone or '?'}  ({source})")
    return 0


def _cmd_session_stop(args: argparse.Namespace) -> int:
    client = _client()
    ident = args.identifier

    # deallocate() takes a phone_id. Accept a session_id too by resolving it against
    # the active list; if that lookup fails, fall back to treating ident as a phone_id.
    phone_id = ident
    try:
        for s in client.phones.active_sessions().sessions or []:
            if ident in (s.session_id, s.phone_id):
                phone_id = s.phone_id
                break
    except ApiError:
        pass

    try:
        client.phones.deallocate(phone_id=phone_id)
    except ApiError as e:
        _err(f"could not release {ident} (HTTP {e.status_code}): {_detail(e)}")
        return 1

    print(f"Released {phone_id}.")
    return 0


# --- helpers --------------------------------------------------------------


def _client() -> Client:
    """Construct a ``Client``, turning the missing-key error into a friendly exit."""
    try:
        return Client()
    except ValueError:
        _err("no API key found. Run `axilio login` or set AXILIO_API_KEY.")
        raise SystemExit(1) from None


def _err(msg: str) -> None:
    """Print an error to stderr, prefixed like a well-behaved CLI."""
    print(f"axilio: {msg}", file=sys.stderr)


def _check(passed: bool, label: str, hint: str = "") -> None:
    mark = "✓" if passed else "✗"
    line = f"  {mark} {label}"
    if not passed and hint:
        line += f"  ({hint})"
    print(line)


def _detail(e: ApiError) -> str:
    """A short, human-readable message pulled from an ``ApiError`` body."""
    body = getattr(e, "body", None)
    if isinstance(body, dict):
        return str(body.get("detail") or body.get("message") or body)
    return str(body) if body else ""
