try:
    import requests
except Exception:
    requests = None

try:
    import torch
except Exception:
    torch = None

import os

try:
    import psutil
except Exception:
    psutil = None


OLLAMA_URL = "http://127.0.0.1:11434/api/generate"
DEFAULT_MODEL = os.getenv("OLLAMA_MODEL", "phi3:mini")
OLLAMA_OPTIONS = {
    "num_ctx": 1024,
    "num_predict": 220,
    "temperature": 0.3,
}


def detect_best_model():
    """
    Automatically choose best Ollama model
    based on machine hardware.
    """

    # default safe model
    model = DEFAULT_MODEL

    try:
        if psutil is None:
            return model

        total_ram_gb = psutil.virtual_memory().total / (1024 ** 3)

        has_gpu = False

        # NVIDIA GPU detection
        if torch is not None:
            has_gpu = torch.cuda.is_available()

        # powerful system
        if has_gpu and total_ram_gb >= 24:
            model = "mistral"

        # medium system
        elif total_ram_gb >= 12:
            model = DEFAULT_MODEL

        # low-end system
        else:
            model = DEFAULT_MODEL

    except Exception:
        model = DEFAULT_MODEL

    return model


MODEL_NAME = detect_best_model()


def generate_response(prompt: str):

    """
    Generate response using Ollama
    with automatic model selection.
    """

    if requests is None:
        return "LLM ERROR: requests package is not installed"

    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False,
        "keep_alive": 0,
        "options": OLLAMA_OPTIONS,
    }

    try:

        response = requests.post(
            OLLAMA_URL,
            json=payload,
            timeout=180
        )

        if response.status_code == 200:

            result = response.json().get(
                "response",
                ""
            ).strip()

            return result

        error_text = response.text

        if "failed to allocate" in error_text or "llama runner process has terminated" in error_text:
            return (
                "LLM ERROR: Ollama could not allocate enough memory for the model. "
                "Close other apps, restart Ollama, or use a smaller model such as tinyllama. "
                f"Raw Ollama error: {error_text}"
            )

        return f"LLM ERROR: status {response.status_code} | {error_text}"

    except requests.exceptions.Timeout:
        return (
            "LLM ERROR: Ollama took too long to respond. "
            "Try a shorter question, restart Ollama, or use a smaller model."
        )

    except Exception as e:

        return f"LLM ERROR: {str(e)}"
