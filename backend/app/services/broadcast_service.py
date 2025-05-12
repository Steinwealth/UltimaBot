# backend/app/services/broadcast_service.py

from typing import List, Dict
from fastapi import WebSocket
import logging

logger = logging.getLogger(__name__)

class BroadcastService:
    connections: List[WebSocket] = []

    @classmethod
    async def register(cls, websocket: WebSocket):
        await websocket.accept()
        cls.connections.append(websocket)
        logger.info(f"[Broadcast] WebSocket connected. Total: {len(cls.connections)}")

    @classmethod
    async def unregister(cls, websocket: WebSocket):
        if websocket in cls.connections:
            cls.connections.remove(websocket)
            logger.info(f"[Broadcast] WebSocket disconnected. Total: {len(cls.connections)}")

    @classmethod
    async def send_message(cls, message: Dict):
        for ws in cls.connections.copy():
            try:
                await ws.send_json(message)
            except Exception as e:
                logger.warning(f"[Broadcast] Error sending message: {e}")
                await cls.unregister(ws)

    # ----------------------
    # Predefined Events
    # ----------------------
    @classmethod
    async def trade_close(cls, symbol: str, gain_pct: float, gain_usd: float, rationale: str):
        text = f"{symbol} closed {gain_pct:+.1f}% (${gain_usd:+.2f}) — {rationale}"
        sound = "negative.mp3" if gain_pct < 0 else None
        await cls.send_message({
            "event": "trade_closed",
            "symbol": symbol,
            "gain_pct": gain_pct,
            "gain_usd": gain_usd,
            "rationale": rationale,
            "text": text,
            "sound": sound
        })

    @classmethod
    async def win_streak(cls, streak: int):
        messages = {
            10: "Winning Streak for 10 Trades!",
            15: "Brutality!!!",
            20: "Tubular!!!",
            25: "Explosive!!!",
            30: "Groovy!!!",
            35: "€£$¥!!!",
        }
        if streak in messages:
            await cls.send_message({
                "event": "win_streak",
                "streak": streak,
                "text": messages[streak],
                "sound": "win_streak.mp3"
            })

    @classmethod
    async def generic_alert(cls, text: str, sound: str = None):
        await cls.send_message({
            "event": "alert",
            "text": text,
            "sound": sound
        })
