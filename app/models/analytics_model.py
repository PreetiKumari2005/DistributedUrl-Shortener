
from sqlalchemy import Column, String, DateTime, BigInteger
from sqlalchemy.sql import func
from app.database.db import Base

class ClickEvent(Base):
    __tablename__ = "click_events"

    id         = Column(BigInteger, primary_key=True, autoincrement=True)
    short_code = Column(String(10), nullable=False)
    clicked_at = Column(DateTime(timezone=True), server_default=func.now())
    user_agent = Column(String, nullable=True)
    referrer   = Column(String, nullable=True)
