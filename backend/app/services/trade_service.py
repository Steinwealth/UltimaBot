# backend/app/services/trade_service.py

from typing import List, Dict
from app.utils.broker_clients.broker_manager import BrokerManager
from app.services.websocket_service import WebSocketService

class TradeService:

    @staticmethod
    async def get_trades_for_broker(broker_id: str) -> List[Dict]:
        """
        Retrieve all open trades for a broker.
        """
        broker_client = BrokerManager.get_client(broker_id)
        if not broker_client:
            raise ValueError(f"Broker {broker_id} not found")

        return await broker_client.list_open_trades()

    @staticmethod
    async def execute_trade(broker_id: str, symbol: str, quantity: float, side: str) -> Dict:
        """
        Execute a buy or sell trade.
        """
        broker_client = BrokerManager.get_client(broker_id)
        if not broker_client:
            raise ValueError(f"Broker {broker_id} not found")

        if side.lower() not in ["buy", "sell"]:
            raise ValueError("Side must be 'buy' or 'sell'")

        result = await broker_client.open_trade(symbol, quantity, side=side.lower())
        await WebSocketService.broadcast(broker_id, {
            "action": "trade_executed",
            "data": result
        })
        return result

    @staticmethod
    async def close_trade(broker_id: str, trade_id: str) -> Dict:
        """
        Close a trade.
        """
        broker_client = BrokerManager.get_client(broker_id)
        if not broker_client:
            raise ValueError(f"Broker {broker_id} not found")

        result = await broker_client.close_trade(trade_id)
        await WebSocketService.broadcast(broker_id, {
            "action": "trade_closed",
            "data": result
        })
        return result
