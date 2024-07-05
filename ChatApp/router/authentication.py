from typing import Collection
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from ChatApp import database, tokens
from ChatApp.hashing import Hash

router = APIRouter(tags=['Authentication'])

@router.post("/login")
def login(request: OAuth2PasswordRequestForm = Depends(), collection: Collection = Depends(database.get_db)):
    query = {"email": request.username}
    user = collection.find_one(query)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Credentials")
    if not Hash.verify(user["password"], request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Incorrect Password")
    
    access_token = tokens.create_access_token(data={"sub": user["email"]})
    # response = RedirectResponse(url="/auth/protected")
    # response.set_cookie(key="Authorization", value=f"Bearer {access_token}", httponly=True)
    # return response

    return {'status': "Successfully Logged in", 'access_token': access_token, 'token_type': "bearer"}

