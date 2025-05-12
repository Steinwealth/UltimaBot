# backend/app/services/marquee_service.py

from typing import List, Dict, Union
from fastapi import WebSocket
import logging

class MarqueeService:
    connections: List[WebSocket] = []

    @classmethod
    async def connect(cls, websocket: WebSocket):
        try:
            await websocket.accept()
            cls.connections.append(websocket)
            logging.info("[MarqueeService] Client connected.")
        except Exception as e:
            logging.error(f"[MarqueeService] WebSocket accept failed: {e}")

    @classmethod
    def disconnect(cls, websocket: WebSocket):
        if websocket in cls.connections:
            cls.connections.remove(websocket)
            logging.info("[MarqueeService] Client disconnected.")

    @classmethod
    async def broadcast(cls, message: Union[str, Dict]):
        """
        Broadcasts either a simple text string or a full dict with keys like:
        {"text": "...", "sound": "file.mp3"}
        """
        payload = {"text": message} if isinstance(message, str) else message
        stale_connections = []

        for ws in cls.connections:
            try:
                await ws.send_json(payload)
            except Exception as e:
                stale_connections.append(ws)
                logging.warning(f"[MarqueeService] Failed to send message: {e}")

        for ws in stale_connections:
            cls.disconnect(ws)
