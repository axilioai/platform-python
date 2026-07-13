"""axilio.cli: argument parsing and command behaviour, without touching the network."""

from __future__ import annotations

import types

from axilio import _config
from axilio.cli import _app


def test_no_command_prints_help(capsys):
    assert _app.main([]) == 2
    assert "usage" in capsys.readouterr().out.lower()


def test_login_rejects_non_axl_key(capsys):
    # A bad prefix is caught before any network call is made.
    assert _app.main(["login", "--api-key", "nope"]) == 1
    assert "Axilio key" in capsys.readouterr().err


class _FakeBalance:
    balance_display = "$0.65"


class _FakeClient:
    def __init__(self, **_kwargs):
        self.base_url = "https://api.axilio.ai"
        self.billing = types.SimpleNamespace(get_balance=lambda: _FakeBalance())


def test_login_success_saves_config(tmp_path, monkeypatch, capsys):
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path))
    monkeypatch.setattr(_app, "Client", _FakeClient)
    assert _app.main(["login", "--api-key", "axl_good"]) == 0
    assert _config.load_api_key() == "axl_good"
    assert "Balance: $0.65" in capsys.readouterr().out


def test_doctor_without_key_fails(tmp_path, monkeypatch):
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path))
    monkeypatch.delenv("AXILIO_API_KEY", raising=False)
    assert _app.main(["doctor"]) == 1


def test_session_start_prints_live_view(monkeypatch, capsys):
    alloc = types.SimpleNamespace(
        session_id="sess_1",
        phone_id="phone_1",
        region="us-east",
        live_view_url="https://app.axilio.ai/live/tok",
        control_url="wss://connect/ws",
    )
    client = types.SimpleNamespace(phones=types.SimpleNamespace(allocate=lambda **_kw: alloc))
    monkeypatch.setattr(_app, "Client", lambda **_kw: client)
    assert _app.main(["session", "start", "--phone-type", "android"]) == 0
    out = capsys.readouterr().out
    assert "sess_1" in out
    assert "live/tok" in out
