import getpass
import subprocess


def get_api_key(service_name: str) -> str:
    """
    Retrieve an API key from macOS Keychain.
    """
    try:
        result = subprocess.run(
            [
                "security",
                "find-generic-password",
                "-a",
                getpass.getuser(),
                "-s",
                service_name,
                "-w",
            ],
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        raise RuntimeError(
            "API key not found in Keychain for service "
            f"'{service_name}'.\n\n"
            "Pour ajouter une clé API :\n"
            "- Dans Alfred, tape `sp setup`, choisis le fournisseur correspondant "
            "et enregistre ta clé (elle sera stockée dans le Trousseau macOS).\n"
            "- Ou via le terminal, par exemple :\n"
            "  security add-generic-password -a \"$USER\" -s "
            f"\"{service_name}\" -w \"VOTRE_CLE_API\""
        )
