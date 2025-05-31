# core/events/pubsub.py
import json
import threading
from core.memory.redis_client import redis_client
from core.logging import setup_logger

logger = setup_logger("pubsub")

def publish(channel: str, payload: dict):
    message = json.dumps(payload)
    redis_client.publish(channel, message)
    logger.info(f"Published to {channel}: {message}")

def subscribe(channel: str, callback):
    pubsub = redis_client.pubsub()
    pubsub.subscribe(channel)

    def listen():
        for message in pubsub.listen():
            if message["type"] == "message":
                try:
                    data = json.loads(message["data"])
                    callback(data)
                except Exception as e:
                    logger.error(f"Failed to handle message: {e}")

    thread = threading.Thread(target=listen, daemon=True)
    thread.start()
    logger.info(f"Subscribed to {channel}")
