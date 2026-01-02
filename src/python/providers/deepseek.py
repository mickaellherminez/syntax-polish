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
            log_response_metadata("DeepSeek", body, debug)
            data = json.loads(body)
    except json.JSONDecodeError as exc:
        raise RuntimeError("Réponse DeepSeek illisible (JSON invalide).") from exc
    except urllib.error.HTTPError as exc:
        error_body = exc.read()
        log_response_metadata("DeepSeek HTTP error", error_body, debug)
        raise RuntimeError(f"HTTP Error {exc.code}: requête refusée par DeepSeek.") from exc
    except (urllib.error.URLError, TimeoutError) as exc:
        raise RuntimeError("Erreur réseau lors de l'appel DeepSeek.") from exc

    choices = data.get("choices") if isinstance(data, dict) else None
    if not isinstance(choices, list) or not choices:
        raise RuntimeError("Réponse DeepSeek invalide : champ 'choices' manquant.")

    first_choice = safe_get_first_item(choices, "Réponse DeepSeek vide.")
    message = first_choice.get("message") if isinstance(first_choice, dict) else None
    content = message.get("content") if isinstance(message, dict) else None
    if not isinstance(content, str):
        raise RuntimeError("Réponse DeepSeek invalide : contenu manquant.")

    return content



