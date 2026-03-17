from bson import ObjectId
from django.conf import settings
from pymongo import MongoClient

class UserRepository:
    def __init__(self):
        # Extrae de core/settings.py o usa defaults
        uri = getattr(settings, 'MONGO_URI', 'mongodb://localhost:27017')
        db_name = getattr(settings, 'MONGO_DB_NAME', 'local')
        self.client = MongoClient(uri)
        self.db = self.client[db_name]
        self.collection = self.db['users']

    def get_all(self):
        return list(self.collection.find())

    def get_by_id(self, user_id: str):
        try:
            return self.collection.find_one({"_id": ObjectId(user_id)})
        except Exception:
            return None

    def get_by_email(self, email: str):
        return self.collection.find_one({"email": email})

    def create(self, user_data: dict):
        result = self.collection.insert_one(user_data)
        return self.get_by_id(result.inserted_id)

    def update(self, user_id: str, user_data: dict):
        self.collection.find_one_and_replace({"_id": ObjectId(user_id)}, user_data)
        return self.get_by_id(user_id)

    def delete(self, user_id: str):
        result = self.collection.find_one_and_delete({"_id": ObjectId(user_id)})
        return result is not None