from fastapi import APIRouter, Depends, Form, HTTPException, Request
from pymongo.collection import Collection
from ChatApp.models import User, Login
from ChatApp.database import get_db
from ChatApp.schemas import list_serial
from bson import ObjectId
from ChatApp.hashing import Hash
from ChatApp import oauth2

router = APIRouter(
    prefix="/user",
    tags=['Users']
)

# GET Request Method
@router.get("/get")
async def get_users(collection: Collection = Depends(get_db), current_user: Login = Depends(oauth2.get_current_user)):
    users = list_serial(collection.find())
    return users

# POST Request Method
@router.post("/create")
async def create_user(user: User, collection: Collection = Depends(get_db), current_user: Login = Depends(oauth2.get_current_user)):
    pwd = Hash.bcrypt(user.password)
    user.password = pwd
    collection.insert_one(dict(user))
    return user


# PUT Request Method
@router.put("/update/{id}")
async def update_user(id: str, user: User, collection: Collection = Depends(get_db), current_user: Login = Depends(oauth2.get_current_user)):
    existing_user = collection.find_one({"_id": ObjectId(id)})
    if existing_user is None:
        raise HTTPException(status_code=404, detail=f"User with id {id} not found")
    
    user.password = Hash.bcrypt(user.password)
    collection.find_one_and_update({"_id": ObjectId(id)}, {"$set": dict(user)})
    return user
    

# DELETE Request Method
@router.delete("/delete/{id}")
async def delete_user(id: str, collection: Collection = Depends(get_db), current_user: Login = Depends(oauth2.get_current_user)):
    user = collection.find_one({"_id": ObjectId(id)})
    if user is None:
        raise HTTPException(status_code=404, detail=f"User with id {id} not found")
    collection.find_one_and_delete({"_id": ObjectId(id)})
    return "User deleted Successfully !!"

#current_user: schemas.User = Depends(oauth2.get_current_user)