# core/agents/registry.py
import yaml
from pathlib import Path

AGENT_CONFIG_PATH = Path("agents/config/agents.yaml")

def load_agent_config():
    with open(AGENT_CONFIG_PATH, "r") as f:
        return yaml.safe_load(f)["agents"]

# Example use
AGENTS = load_agent_config()

def get_agent_model(name: str) -> str:
    return AGENTS[name]["model"]

def get_agent_channels(name: str) -> tuple[str, str | list]:
    return (
        AGENTS[name].get("channel_in"),
        AGENTS[name].get("channel_out")
    )
