from fastapi import FastAPI
from .router import user_route, authentication

app = FastAPI()
app.include_router(user_route.router)
app.include_router(authentication.router)

