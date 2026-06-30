import os
import redis

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")

try:
    redis_client = redis.from_url(REDIS_URL, decode_responses=True)
    redis_client.ping()
except Exception as e:
    print(f"[REDIS] Warning: could not connect at startup: {e}")
    redis_client = None

CACHE_TTL = 86400

def get_from_cache(short_code: str):
    if not redis_client:
        return None
    try:
        return redis_client.get(f"url:{short_code}")
    except Exception:
        return None

def set_in_cache(short_code: str, long_url: str):
    if not redis_client:
        return
    try:
        redis_client.setex(f"url:{short_code}", CACHE_TTL, long_url)
    except Exception:
        pass

def delete_from_cache(short_code: str):
    if not redis_client:
        return
    try:
        redis_client.delete(f"url:{short_code}")
    except Exception:
        pass
