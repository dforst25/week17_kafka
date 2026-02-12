import json
import os
from confluent_kafka import Producer


producer_config = {
    "bootstrap.servers": os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
}

producer = Producer(producer_config)


def delivery_report(err, msg):
    if err:
        print("Delivery failed: {err}")
    else:
        print(f"Delivered {msg.value().decode('utf-8')}")
        print(f"Delivered to {msg.topic()} : partition {msg.partition()} : at offset {msg.offset()}")


def produce_weapon_json(weapon: dict):
    producer.produce(
        topic=os.getenv("KAFKA_TOPIC", "weapons"),
        value=json.dumps(weapon).encode('utf-8'),
        callback=delivery_report
    )
    producer.flush()


def produce_weapons(weapons: list[dict]):
    for weapon in weapons:
        produce_weapon_json(weapon)
