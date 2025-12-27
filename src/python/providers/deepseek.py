import json
import urllib.request

from utils.keychain import get_api_key


def send_request(text: str) -> str:
    api_key = get_api_key("syntax-polish-deepseek")

    payload = {
        "model": "deepseek-chat",
        "messages": [{"role": "user", "content": text}],
    }

    req = urllib.request.Request(
        url="https://api.deepseek.com/v1/chat/completions",
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


