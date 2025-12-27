import os
import sys

import pytest

import main
import providers


def test_get_input_text_from_argv(monkeypatch):
    monkeypatch.setattr(sys, "argv", ["main.py", "hello", "world"])
    assert main._get_input_text() == "hello world"


@pytest.mark.parametrize(
    "env_value, expected",
    [
        (None, "deepseek"),
        ("deepseek", "deepseek"),
        ("DeepSeek", "deepseek"),
    ],
)
def test_provider_env_default_and_normalisation(monkeypatch, env_value, expected, capsys):
    if env_value is None:
        monkeypatch.delenv("AI_PROVIDER", raising=False)
    else:
        monkeypatch.setenv("AI_PROVIDER", env_value)

    # On force argv pour que _get_input_text lise une chaîne non vide
    monkeypatch.setattr(sys, "argv", ["main.py", "texte"])

    # Pour éviter un appel réseau dans ce test, on monkeypatch le provider
    class DummyProvider:
        @staticmethod
        def send_request(text: str) -> str:  # pragma: no cover - trivial
            assert text == "texte"
            return "OK"

    monkeypatch.setattr(providers, "deepseek", DummyProvider)

    exit_code = main.main()
    captured = capsys.readouterr()

    assert exit_code == 0
    assert captured.out.strip() == "OK"


