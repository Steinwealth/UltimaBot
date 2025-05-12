# backend/app/services/websocket_service.py

from typing import Dict, List
from fastapi import WebSocket, WebSocketDisconnect
import logging

class WebSocketService:
    connections: Dict[str, List[WebSocket]] = {}

    @classmethod
    async def connect(cls, websocket: WebSocket, broker_id: str):
        await websocket.accept()
        cls.connections.setdefault(broker_id, []).append(websocket)
        logging.info(f"WebSocket connected: {broker_id}")

    @classmethod
    def disconnect(cls, websocket: WebSocket, broker_id: str):
        if broker_id in cls.connections:
            cls.connections[broker_id] = [
                ws for ws in cls.connections[broker_id] if ws != websocket
            ]
            if not cls.connections[broker_id]:
                del cls.connections[broker_id]
        logging.info(f"WebSocket disconnected: {broker_id}")

    @classmethod
    async def broadcast(cls, broker_id: str, message: dict):
        if broker_id not in cls.connections:
            return

        stale_sockets = []
        for websocket in cls.connections[broker_id]:
            try:
                await websocket.send_json(message)
            except Exception as e:
                logging.warning(f"Failed to send WebSocket message: {e}")
                stale_sockets.append(websocket)

        # Clean up disconnected clients
        for ws in stale_sockets:
            cls.disconnect(ws, broker_id)
