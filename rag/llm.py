# LLM integration will be implemented here
try:
    import requests
except Exception:
    requests = None


OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "mistral"


def generate_response(prompt: str):
    """
    Generate response using Ollama.
    Safe fallback if Ollama is unavailable.
    """

    if requests is None:
        return "LLM is not available right now. Please try again later."

    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False
    }

    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=60)

        if response.status_code == 200:
            return response.json().get("response", "").strip()

        return "LLM is unavailable right now."

    except Exception:
        return "LLM is not running yet. Business analysis is available, but AI chat is offline."