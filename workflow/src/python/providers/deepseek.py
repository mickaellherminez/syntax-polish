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
    Envoie le texte sélectionné à DeepSeek avec un prompt de correction explicite.
    """
    api_key = get_api_key("syntax-polish-deepseek")

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {
            "role": "user",
            "content": (
                "Voici un texte à corriger et éventuellement légèrement améliorer. "
                "Ne change pas le sens ni le format plus que nécessaire.\n\n"
                f"{text}"
            ),
        },
    ]

    payload = {
        "model": "deepseek-chat",
        "messages": messages,
    }

    data = json.dumps(payload).encode("utf-8")

    req = urllib.request.Request(
        url="https://api.deepseek.com/v1/chat/completions",
        data=data,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    debug = os.getenv("DEBUG", "0") == "1"

    try:
        with urllib.request.urlopen(req, timeout=20) as response:
            body = response.read()
            if debug:
                print(f"[DEBUG] DeepSeek raw response: {body[:500]!r}")
            data = json.loads(body)
            return data["choices"][0]["message"]["content"]
    except urllib.error.HTTPError as exc:
        if debug:
            error_body = exc.read()
            print(f"[DEBUG] DeepSeek HTTP {exc.code} body: {error_body[:500]!r}")
        raise RuntimeError(f"HTTP Error {exc.code}: Bad Request") from exc


