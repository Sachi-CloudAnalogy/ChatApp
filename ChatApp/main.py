from fastapi import FastAPI
from .router import user_route, authentication, msg_route

app = FastAPI()
app.include_router(user_route.router)
app.include_router(authentication.router)
app.include_router(msg_route.router)
