"""axilio._config: the CLI credential store shared with Client resolution."""

from __future__ import annotations

import stat

from axilio import _config


def test_missing_config_reads_empty(tmp_path, monkeypatch):
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path))
    assert _config.load_config() == {}
    assert _config.load_api_key() is None
    assert _config.load_base_url() is None


def test_save_and_load_roundtrip(tmp_path, monkeypatch):
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path))
    path = _config.save_config({"api_key": "axl_abc", "base_url": "https://example.test"})
    assert path == _config.config_path()
    assert _config.load_api_key() == "axl_abc"
    assert _config.load_base_url() == "https://example.test"


def test_saved_file_is_owner_only(tmp_path, monkeypatch):
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path))
    path = _config.save_config({"api_key": "axl_abc"})
    assert stat.S_IMODE(path.stat().st_mode) == 0o600


def test_corrupt_config_reads_empty(tmp_path, monkeypatch):
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path))
    path = _config.config_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("not json{", encoding="utf-8")
    assert _config.load_config() == {}
