
import os
import redis

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
redis_client = redis.from_url(REDIS_URL, decode_responses=True)

CACHE_TTL = 86400

def get_from_cache(short_code: str):
    return redis_client.get(f"url:{short_code}")

def set_in_cache(short_code: str, long_url: str):
    redis_client.setex(f"url:{short_code}", CACHE_TTL, long_url)

def delete_from_cache(short_code: str):
    redis_client.delete(f"url:{short_code}")