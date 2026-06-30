
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.database.db import get_db
from app.services.url_service import create_short_url, get_long_url
from app.services.kafka_producer import send_click_event
from app.config import settings

router = APIRouter()

class ShortenRequest(BaseModel):
    long_url: str

@router.post("/shorten")
def shorten_url(request: ShortenRequest, db: Session = Depends(get_db)):
    code = create_short_url(request.long_url, db)
    return {
        "short_url": f"{settings.base_url}/{code}",
        "short_code": code,
        "long_url": request.long_url
    }

@router.get("/health")
def health_check():
    return {"status": "ok"}

@router.get("/{short_code}")
def redirect_url(short_code: str, request: Request, db: Session = Depends(get_db)):
    long_url = get_long_url(short_code, db)
    if not long_url:
        raise HTTPException(status_code=404, detail="URL not found")

    # send analytics to kafka (async, won't crash if kafka is down)
    send_click_event(
        short_code=short_code,
        user_agent=request.headers.get("user-agent", ""),
        referrer=request.headers.get("referer", "")
    )

    return RedirectResponse(url=long_url, status_code=302)
