"""Fonctions utilitaires partagées entre les fournisseurs IA."""

from __future__ import annotations

import json
from typing import Any, Iterable


def log_response_metadata(source: str, body: bytes, debug: bool) -> None:
    """Journalise des méta-informations non sensibles sur une réponse HTTP."""

    if not debug:
        return

    metadata: dict[str, Any] = {
        "length": len(body),
    }

    try:
        parsed = json.loads(body)
    except Exception:
        metadata["note"] = "corps non JSON"
    else:
        if isinstance(parsed, dict):
            metadata["keys"] = sorted(parsed.keys())
        metadata["type"] = type(parsed).__name__

    print(f"[DEBUG] {source} response metadata: {metadata}")


def safe_get_first_item(seq: Iterable[Any], error_message: str) -> Any:
    """Récupère le premier élément d'une séquence ou lève une erreur claire."""

    for item in seq:
        return item
    raise RuntimeError(error_message)
