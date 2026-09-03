import httpx
OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "gemma3:4b"

def generate_response(prompt: str):
    payload = {
            "model": MODEL,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "stream": False
    }
    
    response = httpx.post(
            OLLAMA_URL,
            json=payload,
            timeout=120.0
            )
    
    response.raise_for_status()
    data = response.json()
    return data["message"]["content"]

