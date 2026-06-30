
import json
from datetime import datetime

def send_click_event(short_code: str, user_agent: str = "", referrer: str = ""):
    try:
        from kafka import KafkaProducer
        from app.config import settings

        producer = KafkaProducer(
            bootstrap_servers=settings.kafka_bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode("utf-8")
        )

        event = {
            "short_code": short_code,
            "user_agent": user_agent,
            "referrer": referrer,
            "timestamp": datetime.utcnow().isoformat()
        }

        producer.send(settings.kafka_topic, value=event)
        producer.flush()
        print(f"[KAFKA] Sent click event for {short_code}")

    except Exception as e:
        # kafka is optional — don't crash if not running
        print(f"[KAFKA] Skipped (Kafka not running): {e}")
