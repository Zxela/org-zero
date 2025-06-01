import requests
import json
from core.config import get_settings

class ModelService:
    def __init__(self):
        settings = get_settings()
        self.backend = settings.MODEL_BACKEND
        self.api_key = settings.OPENROUTER_API_KEY
        self.base_url = "https://openrouter.ai/api/v1"
        self.default_headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def chat(self, model: str, messages: list[dict]) -> str:
        if self.backend == "openrouter":
            return self._call_openrouter(model, messages)
        raise ValueError(f"Unsupported backend: {self.backend}")

    def _call_openrouter(self, model: str, messages: list[dict]) -> str:
        url = f"{self.base_url}/chat/completions"
        payload = {
            "model": model,
            "messages": messages,
        }

        print("🛠️ OpenRouter request payload:")
        print(json.dumps(payload, indent=2))

        try:
            print("🚀 Requesting OpenRouter with:")
            print("Model:", model)
            print("Messages:", json.dumps(messages, indent=2))
            print("API Key Present:", bool(self.api_key))

            response = requests.post(url, headers=self.default_headers, json=payload)
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"]
        except requests.exceptions.RequestException as e:
            print("❌ OpenRouter request failed:")
            if e.response is not None:
                print(f"Status: {e.response.status_code}")
                print(f"Response: {e.response.text}")
            else:
                print(str(e))
            raise


    def _call_ollama(self, model: str, messages: list[dict]) -> str:
        data = {
            "model": model,
            "messages": messages,
        }

        try:
            response = requests.post(self.ollama_url, json=data)
            response.raise_for_status()
            return response.json()["message"]["content"]
        except requests.exceptions.RequestException as e:
            print("❌ Ollama request failed:")
            if e.response is not None:
                print(f"Status: {e.response.status_code}")
                print(f"Response: {e.response.text}")
            else:
                print(str(e))
            raise
