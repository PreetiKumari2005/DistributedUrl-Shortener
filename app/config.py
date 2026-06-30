
import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    database_url: str = "postgresql://admin:admin123@127.0.0.1:5432/urlshortener"
    redis_url: str = "redis://localhost:6379"
    kafka_bootstrap_servers: str = "localhost:9092"
    kafka_topic: str = "click_events"
    base_url: str = "http://localhost:8000"

settings = Settings()