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
            f"API key not found in Keychain for service '{service_name}'."
        )
