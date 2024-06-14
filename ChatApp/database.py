from typing import Collection
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")

db = client.user_db
collection = db["user_collection"]

def get_db() -> Collection:
    return collection    

