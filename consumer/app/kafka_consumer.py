from confluent_kafka import Consumer
import json
import os
from mysql_connection import DbConnection


def insert_document_by_type(document: dict, db: DbConnection):
    document_type = document.pop("type")
    if document_type == "customer":
        db.insert_customer(tuple(document.values()))
        print("insert a customer")
    if document_type == "order":
        db.insert_order(tuple(document.values()))
        print("insert a order")


def get_and_insert_orders_and_costumer(consumer: Consumer, db: DbConnection):
    consumer.subscribe([os.getenv("KAFKA_TOPIC", "weapons")])

    print("Consumer is running and subscribed to weapon topic")

    try:
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                print("Error:", msg.error())
                continue

            value = msg.value().decode("utf-8")
            document = json.loads(value)
            if "type" not in document:
                print("Error: Not all required fields exists")
                continue
            insert_document_by_type(document, db)
    except KeyboardInterrupt:
        print("Stopping consumer")

    finally:
        consumer.close()
