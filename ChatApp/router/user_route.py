from fastapi import APIRouter, Depends, HTTPException
from pymongo import ReturnDocument
from pymongo.collection import Collection

from ChatApp import oauth2
from ..models import User
from ..database import get_db
from ..schemas import list_serial
from bson import ObjectId
from ..hashing import Hash

router = APIRouter(
    prefix="/user",
    tags=['Users']
)

# GET Request Method
@router.get("/")
async def get_users_list(collection: Collection = Depends(get_db)):
    users = list_serial(collection.find())
    return users

# POST Request Method
@router.post("/create")
async def SignUp(user: User, collection: Collection = Depends(get_db)):
    pwd = Hash.bcrypt(user.password)
    user.password = pwd
    collection.insert_one(dict(user))
    return user


# PUT Request Method
@router.put("/update")
async def update_details(user: User, collection: Collection = Depends(get_db), current_user: User = Depends(oauth2.get_current_user)):
    # existing_user = collection.find_one({"email": current_user['email']})
    user.password = Hash.bcrypt(user.password)
    user.email = current_user['email']
    collection.find_one_and_update({"email": current_user['email']}, {"$set": dict(user)})
    return user
    

# DELETE Request Method
# @router.delete("/delete/{id}")
# async def delete_user(id: str, collection: Collection = Depends(get_db)):
#     user = collection.find_one({"_id": ObjectId(id)})
#     if user is None:
#         raise HTTPException(status_code=404, detail=f"User with id {id} not found")
#     collection.find_one_and_delete({"_id": ObjectId(id)})
#     return "User deleted Successfully !!"

#current_user: schemas.User = Depends(oauth2.get_current_user)