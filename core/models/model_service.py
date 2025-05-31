import os
import requests
import json

class ModelService:
    def __init__(self):
        self.backend = os.getenv("MODEL_BACKEND", "openrouter")  # "ollama" or "openrouter"
        self.openrouter_url = "https://openrouter.ai/api/v1/chat/completions"
        self.ollama_url = "http://localhost:11434/api/chat"

        self.headers = {
            "Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY', '')}",
            "Content-Type": "application/json",
        }

    def chat(self, model: str, messages: list[dict]) -> str:
        if self.backend == "ollama":
            return self._call_ollama(model, messages)
        else:
            return self._call_openrouter(model, messages)

    def _call_openrouter(self, model: str, messages: list[dict]) -> str:
        data = {
            "model": model,
            "messages": messages,
        }
        response = requests.post(self.openrouter_url, headers=self.headers, json=data)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]

    def _call_ollama(self, model: str, messages: list[dict]) -> str:
        data = {
            "model": model,
            "messages": messages,
        }
        response = requests.post(self.ollama_url, json=data)
        response.raise_for_status()
        return response.json()["message"]["content"]
