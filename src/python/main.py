import os
import sys


def _get_input_text() -> str:
    """
    Read input from Alfred.

    Depending on the Script Action configuration, Alfred can pass text as arguments
    or via stdin. We support both.
    """
    if len(sys.argv) > 1:
        return " ".join(sys.argv[1:]).strip()
    return sys.stdin.read().strip()


def main() -> int:
    # Ensure imports work even when executed from the repo root:
    # `python3 src/python/main.py ...`
    sys.path.insert(0, os.path.dirname(__file__))

    from providers import get_provider

    text = _get_input_text()
    if not text:
        print("Erreur : aucun texte fourni.")
        return 1

    provider_name = os.getenv("AI_PROVIDER", "deepseek").strip()

    try:
        provider = get_provider(provider_name)
        result = provider.send_request(text)

        print(result)
        return 0
    except ValueError as exc:
        print(f"Erreur : {exc}")
        return 1
    except Exception as exc:
        # UX Alfred: pas de stack trace brute.
        message = str(exc).strip() or "Erreur inconnue."
        print(f"Erreur : {message}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
