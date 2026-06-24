import redis

from src.config.settings import settings

redis_client = redis.Redis.from_url(
    settings.REDIS_URL
)