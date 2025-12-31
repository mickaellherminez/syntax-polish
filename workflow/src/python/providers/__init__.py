"""Interfaces et registre des fournisseurs IA (version workflow)."""
import sys
from typing import Protocol, runtime_checkable

from . import anthropic, deepseek, openai


@runtime_checkable
class Provider(Protocol):
    """Contrat minimal pour les fournisseurs IA."""

    def send_request(self, text: str) -> str:
        """Envoie une requête au fournisseur et retourne la réponse brute."""


_PROVIDERS = {
    "deepseek",
    "openai",
    "anthropic",
}


def get_provider(name: str) -> Provider:
    """Retourne le provider correspondant ou une erreur descriptive."""
    provider = name.strip().lower()
    if provider not in _PROVIDERS:
        available = ", ".join(sorted(_PROVIDERS)) or "aucun"
        raise ValueError(
            f"Fournisseur IA inconnu : {provider}. Fournisseurs disponibles : {available}."
        )

    return getattr(sys.modules[__name__], provider)


__all__ = [
    "Provider",
    "get_provider",
]
