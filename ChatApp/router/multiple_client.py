from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
import uvicorn

from ChatApp import oauth2, models

router = APIRouter(
    prefix="/chat",
    tags=['Chats']
)

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <form id="form" action="" onsubmit="startChat(event)">
            <label for="username">Username:</label>
            <input type="text" id="username" autocomplete="off" required/>
            <button type="submit">Join Chat</button>
        </form>
        <h2>Your Name: <span id="ws-name"></span></h2>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var ws;
            function startChat(event) {
                var username = document.getElementById("username").value;
                document.querySelector("#ws-name").textContent = username;
                ws = new WebSocket(`ws://localhost:8000/ws/${username}`);
                ws.onmessage = function(event) {
                    var messages = document.getElementById('messages');
                    var message = document.createElement('li');
                    var content = document.createTextNode(event.data);
                    message.appendChild(content);
                    messages.appendChild(message);
                };
                document.getElementById("form").style.display = 'none';
                event.preventDefault();
            }
            function sendMessage(event) {
                var input = document.getElementById("messageText");
                ws.send(input.value);
                input.value = '';
                event.preventDefault();
            }
        </script>
    </body>
</html>
"""

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

@router.get("/")
async def get():
    return HTMLResponse(html)

@router.websocket("/ws/{username}")
async def websocket_endpoint(websocket: WebSocket, username: str, current_user: models.Login = Depends(oauth2.get_current_user)):
    await manager.connect(websocket)
    await manager.broadcast(f"{username} joined the chat")
    try:
        while True:
            data = await websocket.receive_text()
            # await manager.send_personal_message(f"You wrote: {data}", websocket)
            await manager.broadcast(f"{username} says: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"{username} left the chat")

if __name__ == "__main__":
    uvicorn.run(router, host="127.0.0.1", port=8000)
