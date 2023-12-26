from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from fastapi.responses import HTMLResponse
from sqlalchemy.engine import row
from sqlalchemy.orm import Session

from .models import MessagesBase
from ..finances import tables
from ..finances.database import get_session

router = APIRouter(
    prefix='/ws_chat',
    tags=['Chat']
)


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

    async def broadcast(self, message: str, add_to_db: bool):
        if add_to_db:
            await self.add_messages_to_database(message)
        for connection in self.active_connections:
            await connection.send_text(message)

    @staticmethod
    async def add_messages_to_database(message: str):
        generator = get_session()
        session = next(generator)
        message_m = tables.Messages(
            message=message
        )
        session.add(message_m)
        session.commit()


manager = ConnectionManager()


@router.get("/last_messages")
async def get_last_messages(session: Session = Depends(get_session)):
    messages = (
        session
        .query(tables.Messages)
        .order_by(tables.Messages.id.desc()).limit(5).all()
    )
    return messages


@router.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket)
    await manager.broadcast(f"Client #{client_id} joined the chat", add_to_db=False)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message(f"You wrote: {data}", websocket)
            await manager.broadcast(f"Client #{client_id} says: {data}", add_to_db=True)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{client_id} left the chat", add_to_db=False)
