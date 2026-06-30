
import redis
from app.config import settings

redis_client = redis.from_url(settings.redis_url, decode_responses=True)

CACHE_TTL = 86400  # 24 hours

def get_from_cache(short_code: str):
    value = redis_client.get(f"url:{short_code}")
    if value:
        print(f"[REDIS] Cache HIT for {short_code}")
    else:
        print(f"[REDIS] Cache MISS for {short_code}")
    return value

def set_in_cache(short_code: str, long_url: str):
    redis_client.setex(f"url:{short_code}", CACHE_TTL, long_url)
    print(f"[REDIS] Cached {short_code} for 24 hours")

def delete_from_cache(short_code: str):
    redis_client.delete(f"url:{short_code}")
    print(f"[REDIS] Deleted {short_code} from cache")
