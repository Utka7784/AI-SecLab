
import httpx

OLLAMA_URL = "http://127.0.0.1:11434/api/chat"
MODEL = "gemma3:4b"


def generate_response(prompt: str):
    payload = {
        "model": MODEL,
        "messages": [
            {
                "role": "system",
                "content":(
                    "You are an IP networking assistant. "
                    "Only answer questions related to IP networking. "
                    "Do not answer questions about unrelated topics."
                    )
            },
            {
                "role": "user",
                "content" : prompt
            }

        ],
        "stream": False
    }

    timeout = httpx.Timeout(
        connect=10.0,
        read=180.0,
        write=10.0,
        pool=10.0
    )

    with httpx.Client(
        timeout=timeout,
        trust_env=False
    ) as client:
        response = client.post(
            OLLAMA_URL,
            json=payload
        )

    response.raise_for_status()

    data = response.json()

    return data["message"]["content"]

