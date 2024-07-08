from typing import Collection
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")

db = client.user_db   #database

#collections
collection = db["user_collection"]
chat_msgs = db["msg_collection"]


def get_db() -> Collection:
    return collection    

def get_msg() -> Collection:
    return chat_msgs
