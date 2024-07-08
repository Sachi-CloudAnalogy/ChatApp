import datetime

def individual_serial(user) -> dict:
    return {
        "id": str(user["_id"]),
        "name": user["name"],
        "email": user["email"],
        "password": user["password"]
    }

def list_serial(users) -> list:
    return [individual_serial(user) for user in users]


def Chat_app(message) -> dict:
    return {
        "id": str(message["_id"]),
        "time": message["time"],
        "sender": message["sender"],
        "receiver": message["receiver"],
        "body": message["body"]
    }

def list_msg(msgs) -> list:
    return [Chat_app(message) for message in msgs]
