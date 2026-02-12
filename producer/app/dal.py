from mongo_connection import MongoConnector
import os
import time
from kafka_publisher import produce_weapons

MONGO_COLLECTION = os.getenv("MONGO_COLLECTION", "users")
CNX = MongoConnector()


def read_all_weapons_with_batches_and_publish():
    weapons = CNX.get_coll(MONGO_COLLECTION)
    size = weapons.count_documents({})
    for i in range(0, size, 40):
        batche = weapons.find({}, {'_id': 0}).skip(i).limit(i + 40)
        produce_weapons(batche)
        time.sleep(0.5)
