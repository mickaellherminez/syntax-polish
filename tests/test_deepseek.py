import json
from unittest import mock

from providers import deepseek


def test_send_request_builds_messages_and_returns_content(monkeypatch):
    # Empêche l’accès réel au Trousseau macOS
    monkeypatch.setattr(deepseek, "get_api_key", lambda service: "TEST_KEY")

    fake_payload = {
        "choices": [{"message": {"content": "Texte corrigé"}}],
    }

    class DummyResponse:
        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            return False

        def read(self) -> bytes:
            return json.dumps(fake_payload).encode()

    with mock.patch("urllib.request.urlopen", return_value=DummyResponse()) as urlopen_mock:
        result = deepseek.send_request("Texte à corriger")

    # Vérifie le contenu renvoyé
    assert result == "Texte corrigé"

    # Vérifie que l'appel HTTP a bien été effectué
    assert urlopen_mock.call_count == 1


