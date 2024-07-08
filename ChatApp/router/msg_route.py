import datetime
from fastapi import APIRouter, Depends, HTTPException
from pymongo.collection import Collection
from ChatApp import oauth2
from ChatApp.tokens import decode_data
from ..models import messages, User
from ..database import get_msg
from ..schemas import list_msg
from bson import ObjectId

router = APIRouter(
    prefix="/chat",
    tags=['Chats']
)

# GET Request Method
@router.get("/")
async def get_all_msgs(collection: Collection = Depends(get_msg), current_user: User = Depends(oauth2.get_current_user)):
    #user = decode_data(current_user)
    # print(current_user)
    query = {"$or": [{"sender": current_user['email']}, {"receiver": current_user['email']}]}
    msgs = list_msg(collection.find(query, sort=[("time", -1)]))
    # msgs = list_msg(collection.find())
    return msgs


# POST Request Method
@router.post("/send")
async def send_msg(msg: messages, collection: Collection = Depends(get_msg), current_user: User = Depends(oauth2.get_current_user)):
    msg.sender = current_user['email']
    collection.insert_one(dict(msg))
    return msg

@router.get("/fetch/{receiver}")
async def fetch_last_msg(receiver: str, collection: Collection = Depends(get_msg), current_user: User = Depends(oauth2.get_current_user)):
    query = {"$and": [{"sender": current_user['email']}, {"receiver": receiver}]}
    message = collection.find_one(query, sort=[("time", -1)])
    if message:
        message['_id'] = str(message['_id'])
        return message
    else:
        raise HTTPException(status_code=404, detail="Message not found")

# PUT Request Method
@router.put("/update/{id}")
async def update_msg(id: str, msg: messages, collection: Collection = Depends(get_msg), current_user: User = Depends(oauth2.get_current_user)):
    update_data = {"body": msg.body} 
    collection.find_one_and_update({"_id": ObjectId(id)}, {"$set": update_data})
    return f"Updated message : {msg.body}"
    

# DELETE Request Method
@router.delete("/delete{receiver}")
async def delete_user(receiver: str, collection: Collection = Depends(get_msg), current_user: User = Depends(oauth2.get_current_user)):
    query = {
        "sender": current_user['email'],
        "receiver": receiver
    }
    last_msg = collection.find_one(query, sort=[("time", -1)])
    collection.find_one_and_delete({"_id": last_msg["_id"]})
    return "Message deleted Successfully !!"

#current_user: schemas.User = Depends(oauth2.get_current_user)