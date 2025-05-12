backend/app/api/routes/websocket.py

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.services.broadcast_service import BroadcastService

router = APIRouter()

@router.websocket("/ws/marquee")
async def marquee_socket(websocket: WebSocket):
    await BroadcastService.register(websocket)
    try:
        while True:
            await websocket.receive_text()  # Keep alive
    except WebSocketDisconnect:
        BroadcastService.unregister(websocket)
