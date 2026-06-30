
import random
import string
from sqlalchemy.orm import Session
from app.models.url_model import URLMapping
from app.services.cache_service import get_from_cache, set_in_cache

def generate_short_code(length=7):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choices(chars, k=length))

def create_short_url(long_url: str, db: Session):
    # generate unique code
    while True:
        code = generate_short_code()
        exists = db.query(URLMapping).filter_by(short_code=code).first()
        if not exists:
            break

    # save to database
    url_mapping = URLMapping(short_code=code, long_url=long_url)
    db.add(url_mapping)
    db.commit()
    db.refresh(url_mapping)

    # save to redis cache
    set_in_cache(code, long_url)
    print(f"[DB] Created short code: {code} for {long_url}")
    return code

def get_long_url(short_code: str, db: Session):
    # check redis cache first
    cached = get_from_cache(short_code)
    if cached:
        return cached

    # fall back to database
    print(f"[DB] Looking up {short_code} in database")
    mapping = db.query(URLMapping).filter_by(
        short_code=short_code,
        is_active=True
    ).first()

    if not mapping:
        return None

    # store in cache for next time
    set_in_cache(short_code, mapping.long_url)
    return mapping.long_url
