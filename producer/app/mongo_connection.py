from pymongo import MongoClient
import os
import json


class MongoConnector:
    def __init__(self):
        self.db_name = os.getenv("DATABASE_NAME", "weapons_db")
        self.mongo_url = os.getenv("MONGODB_URI", "mongodb://localhost:27017/")
        self.client = None

    @staticmethod
    def load_collection_from_data(db, coll_name):
        with open("data/suspicious_customers_orders.json", 'r') as file:
            weapons = json.load(file)
            db[coll_name].insert_many(weapons)

    def get_client(self):
        if self.client is None:
            self.client = MongoClient(self.mongo_url)
            self.client.admin.command('ping')

        return self.client

    def get_db(self):
        return self.get_client()[self.db_name]

    def get_coll(self, coll_name):
        db = self.get_db()
        if coll_name not in db.list_collection_names():
            self.load_collection_from_data(db, coll_name)
        return self.get_db()[coll_name]

    def check_connection(self):
        if self.client is None:
            raise ConnectionError("Server not connected")
        else:
            self.client.admin.command('ping')
