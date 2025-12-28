import json
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
        "model": "claude-3-5-sonnet-20240620",
        "system": SYSTEM_PROMPT,
        "messages": [
            {
                "role": "user",
                "content": (
                    "Voici un texte à corriger et éventuellement légèrement améliorer. "
                    "Ne change pas le sens ni le format plus que nécessaire.\n\n"
                    f"{text}"
                ),
            }
        ],
    }

    req = urllib.request.Request(
        url="https://api.anthropic.com/v1/messages",
        data=json.dumps(payload).encode(),
        headers={
            "x-api-key": api_key,
            "content-type": "application/json",
            "anthropic-version": "2023-06-01",
        },
        method="POST",
    )

    with urllib.request.urlopen(req, timeout=20) as response:
        data = json.loads(response.read())
        return data["content"][0]["text"]
