import json
import os
import urllib.error
import urllib.request

from utils.keychain import get_api_key


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
            if debug:
                print(f"[DEBUG] Anthropic raw response: {body!r}")
            data = json.loads(body)
            return data["content"][0]["text"]
    except urllib.error.HTTPError as exc:
        if debug:
            error_body = exc.read()
            print(f"[DEBUG] Anthropic HTTP {exc.code} body: {error_body!r}")
        raise RuntimeError(f"HTTP Error {exc.code}: Bad Request") from exc


