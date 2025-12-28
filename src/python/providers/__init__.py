"""Interfaces et registre des fournisseurs IA."""
from typing import Mapping, Protocol, runtime_checkable

from . import deepseek


@runtime_checkable
class Provider(Protocol):
    """Contrat minimal pour les fournisseurs IA."""

    def send_request(self, text: str) -> str:
        """Envoie une requête au fournisseur et retourne la réponse brute."""


_PROVIDERS: Mapping[str, Provider] = {
    "deepseek": deepseek,
}


def get_provider(name: str) -> Provider:
    """Retourne le provider correspondant ou une erreur descriptive."""
    provider = name.strip().lower()
    if provider not in _PROVIDERS:
        available = ", ".join(sorted(_PROVIDERS)) or "aucun"
        raise ValueError(
            f"Fournisseur IA inconnu : {provider}. Fournisseurs disponibles : {available}."
        )
    return _PROVIDERS[provider]


__all__ = [
    "Provider",
    "get_provider",
]
