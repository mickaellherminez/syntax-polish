import json
import os
import urllib.error
import urllib.request

from utils.keychain import get_api_key

from ._shared import log_response_metadata, safe_get_first_item


SYSTEM_PROMPT = (
    "Tu es un assistant spécialisé dans la correction et l'amélioration de texte. "
    "Tu corriges l’orthographe, la grammaire, la ponctuation et le style tout en "
    "préservant strictement le sens et le ton du texte original. "
    "Tu détectes automatiquement la langue du texte fourni et tu réponds dans la "
    "même langue. Ta réponse doit contenir uniquement la version corrigée du texte, "
    "sans commentaires ni explications."
)


def send_request(text: str) -> str:
    """
    Envoie le texte sélectionné à Anthropic avec un prompt de correction explicite.
    """
    api_key = get_api_key("syntax-polish-anthropic")

    payload = {
        "model": "claude-opus-4-5-20251101",
        "max_tokens": 1024,
        "system": SYSTEM_PROMPT,
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": (
                            "Voici un texte à corriger et éventuellement légèrement améliorer. "
                            "Ne change pas le sens ni le format plus que nécessaire.\n\n"
                            f"{text}"
                        ),
                    }
                ],
            }
        ],
    }

    data = json.dumps(payload).encode("utf-8")

    req = urllib.request.Request(
        url="https://api.anthropic.com/v1/messages",
        data=data,
        headers={
            "x-api-key": api_key,
            "content-type": "application/json",
            "anthropic-version": "2023-06-01",
        },
        method="POST",
    )

    debug = os.getenv("DEBUG", "0") == "1"

    try:
        with urllib.request.urlopen(req, timeout=20) as response:
            body = response.read()
            log_response_metadata("Anthropic", body, debug)
            data = json.loads(body)
    except json.JSONDecodeError as exc:
        raise RuntimeError("Réponse Anthropic illisible (JSON invalide).") from exc
    except urllib.error.HTTPError as exc:
        error_body = exc.read()
        log_response_metadata("Anthropic HTTP error", error_body, debug)
        raise RuntimeError(f"HTTP Error {exc.code}: requête refusée par Anthropic.") from exc
    except (urllib.error.URLError, TimeoutError) as exc:
        raise RuntimeError("Erreur réseau lors de l'appel Anthropic.") from exc

    content = data.get("content") if isinstance(data, dict) else None
    if not isinstance(content, list) or not content:
        raise RuntimeError("Réponse Anthropic invalide : champ 'content' manquant.")

    first_block = safe_get_first_item(content, "Réponse Anthropic vide.")
    text = first_block.get("text") if isinstance(first_block, dict) else None
    if not isinstance(text, str):
        raise RuntimeError("Réponse Anthropic invalide : texte manquant.")

    return text
