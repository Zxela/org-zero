# core/agents/base.py
from core.config import get_settings
from core.logging import setup_logger
from core.models.model_service import ModelService
from core.memory.redis_client import redis_client
from core.agents.registry import load_agent_config

AGENT_CONFIG = load_agent_config()

class AgentBase:
    def __init__(self, name: str):
        self.name = name
        self.settings = get_settings()
        self.logger = setup_logger(name)
        self.model = ModelService()
        self.memory = redis_client
        self.config = AGENT_CONFIG[name]
        self.model_name = self.config["model"]
        self.channel_in = self.config.get("channel_in")
        self.channel_out = self.config.get("channel_out")

    def log(self, message: str):
        self.logger.info(message)

    def reply(self, messages: list[dict]) -> str:
        return self.model.chat(model=self.model_name, messages=messages)

    def store_memory(self, key: str, value: str):
        self.memory.set(f"{self.name}:{key}", value)

    def get_memory(self, key: str) -> str:
        return self.memory.get(f"{self.name}:{key}")
