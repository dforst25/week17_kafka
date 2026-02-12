from confluent_kafka import Consumer
import os
from mysql_connection import DbConnection
from kafka_consumer import get_and_insert_orders_and_costumer


def main():
    db = DbConnection()
    db.create_tables()

    consumer_config = {
        "bootstrap.servers": os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092"),
        "group.id": "weapons-tracker",
        "auto.offset.reset": "earliest"
    }

    consumer = Consumer(consumer_config)

    get_and_insert_orders_and_costumer(consumer, db)


if __name__ == "__main__":
    main()
