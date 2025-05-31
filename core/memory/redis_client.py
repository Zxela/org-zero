# core/memory/redis_client.py
import redis
from core.config import get_settings

settings = get_settings()

redis_client = redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    decode_responses=True  # makes values str by default
)
