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
    Envoie le texte sélectionné à OpenAI avec un prompt de correction explicite.
    """
    api_key = get_api_key("syntax-polish-openai")

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
        "model": "gpt-4o-mini",
        "messages": messages,
    }

    req = urllib.request.Request(
        url="https://api.openai.com/v1/chat/completions",
        data=json.dumps(payload).encode(),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    with urllib.request.urlopen(req, timeout=20) as response:
        data = json.loads(response.read())
        return data["choices"][0]["message"]["content"]
