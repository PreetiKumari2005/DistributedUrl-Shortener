
import json

def start_consumer():
    try:
        from kafka import KafkaConsumer
        from app.config import settings

        consumer = KafkaConsumer(
            settings.kafka_topic,
            bootstrap_servers=settings.kafka_bootstrap_servers,
            value_deserializer=lambda v: json.loads(v.decode("utf-8")),
            auto_offset_reset="earliest",
            group_id="analytics-group"
        )

        print("[KAFKA] Consumer started, waiting for events...")
        for message in consumer:
            event = message.value
            print(f"[KAFKA] Click event received: {event}")

    except Exception as e:
        print(f"[KAFKA] Consumer error: {e}")

if __name__ == "__main__":
    start_consumer()
E