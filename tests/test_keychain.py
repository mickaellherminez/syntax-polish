import subprocess

import pytest

from utils import keychain


def test_get_api_key_success(monkeypatch):
    completed = subprocess.CompletedProcess(
        args=["security"],
        returncode=0,
        stdout="CLE_API\n",
    )

    def fake_run(*args, **kwargs):  # pragma: no cover - simple stub
        return completed

    monkeypatch.setattr("subprocess.run", fake_run)

    value = keychain.get_api_key("syntax-polish-deepseek")
    assert value == "CLE_API"


def test_get_api_key_missing_raises_runtime_error(monkeypatch):
    def fake_run(*args, **kwargs):  # pragma: no cover - simple stub
        raise subprocess.CalledProcessError(returncode=1, cmd=args[0])

    monkeypatch.setattr("subprocess.run", fake_run)

    with pytest.raises(RuntimeError) as excinfo:
        keychain.get_api_key("syntax-polish-deepseek")

    assert "syntax-polish-deepseek" in str(excinfo.value)


