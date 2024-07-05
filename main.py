from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import uvicorn
from ChatApp.router import user_route, authentication, multiple_client

app = FastAPI()

# app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(user_route.router)
app.include_router(authentication.router)
app.include_router(multiple_client.router)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
