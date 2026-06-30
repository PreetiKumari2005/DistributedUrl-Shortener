
from sqlalchemy import Column, String, Boolean, DateTime, BigInteger
from sqlalchemy.sql import func
from app.database.db import Base

class URLMapping(Base):
    __tablename__ = "url_mappings"

    id         = Column(BigInteger, primary_key=True, autoincrement=True)
    short_code = Column(String(10), unique=True, nullable=False, index=True)
    long_url   = Column(String, nullable=False)
    is_active  = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())