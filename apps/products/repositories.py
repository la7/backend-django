from bson import ObjectId
from django.conf import settings
from pymongo import MongoClient

class ProductRepository:
    def __init__(self):
        uri = getattr(settings, 'MONGO_URI', 'mongodb://localhost:27017')
        db_name = getattr(settings, 'MONGO_DB_NAME', 'local')
        self.client = MongoClient(uri)
        self.db = self.client[db_name]
        self.collection = self.db['products']

    def get_all(self):
        return list(self.collection.find())

    def get_by_id(self, product_id: str):
        try:
            return self.collection.find_one({"_id": ObjectId(product_id)})
        except Exception:
            return None

    def create(self, product_data: dict):
        result = self.collection.insert_one(product_data)
        return self.get_by_id(result.inserted_id)

    def update(self, product_id: str, product_data: dict):
        self.collection.find_one_and_replace({"_id": ObjectId(product_id)}, product_data)
        return self.get_by_id(product_id)

    def delete(self, product_id: str):
        result = self.collection.find_one_and_delete({"_id": ObjectId(product_id)})
        return result is not None