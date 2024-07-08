import datetime
from typing import Optional
from pydantic import BaseModel

class User(BaseModel):
    name: str
    email: str
    password: str

class Login(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str 

class TokenData(BaseModel):
    email: Optional[str] = None
    
class messages(BaseModel):
    time: datetime.datetime
    sender: str
    receiver: str
    body: str   
