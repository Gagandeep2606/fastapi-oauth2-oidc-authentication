from pymongo import MongoClient
import os

Mongo_URI = os.getenv("MONGO_URI")

client = MongoClient(Mongo_URI)
db = client["auth_db"]
collection = db["users"]
refresh_tokens_collection = db["refresh_tokens"]