from typing import Collection
from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from ChatApp import database

router = APIRouter(
    prefix="/chatting",
    tags=['Chatting']
)

templates = Jinja2Templates(directory="ChatApp/templates")

# LOGIN user
@router.get("/")
async def home(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.post("/")
async def login(username: str = Form(...), password: str = Form(...), collection: Collection = Depends(database.get_db)):
    return RedirectResponse(url = "/login")
    # if username == "user" and password == "pass":
    #     return {"message": "Login successful"}
    # else:
    #     return {"message": "Invalid credentials"}
    
    # query = {"email": request.username}
    # user = collection.find_one(query)
    # if not user:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Credentials")
    # if not Hash.verify(user["password"], request.password):
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Incorrect Password")
    
    # access_token = tokens.create_access_token(data={"sub": user["email"]})
    # return {'status': "Successfully Logged in", 'access_token': access_token, 'token_type': "bearer"}
    
