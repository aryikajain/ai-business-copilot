try:
    import requests
except Exception:
    requests = None


OLLAMA_URL = "http://127.0.0.1:11434/api/generate"
MODEL_NAME = "phi3:mini"

def generate_response(prompt: str):
    """
    Generate response using Ollama.
    Returns real error messages while debugging.
    """

    if requests is None:
        return "LLM ERROR: requests package is not installed"

    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False
    }

    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=180)

        if response.status_code == 200:
            return response.json().get("response", "").strip()

        return f"LLM ERROR: status {response.status_code} | {response.text}"

    except Exception as e:
        return f"LLM ERROR: {str(e)}"