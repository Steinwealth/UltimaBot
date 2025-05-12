# backend/engines/auto_close_engine/trade_closer_loop.py

import asyncio
from typing import Dict
from app.engines.auto_close_engine.auto_close import AutoCloseEngine


class TradeCloserLoop:
    def __init__(self, broker_client, trade_executor):
        self.broker_client = broker_client
        self.trade_executor = trade_executor
        self.auto_close_engine = AutoCloseEngine(broker_client)

    async def monitor_trades(self, poll_interval: float = 5.0):
        """
        Continuously evaluates open trades for closure using AutoCloseEngine.
        """
        while True:
            open_trades: Dict[str, dict] = self.trade_executor.get_open_trades()
            for trade_id, trade in list(open_trades.items()):
                try:
                    await self.auto_close_engine.evaluate_trade(trade)
                except Exception as e:
                    print(f"[AutoClose] Error evaluating trade {trade_id}: {e}")
            await asyncio.sleep(poll_interval)

    def remove_trade(self, trade_id: str):
        """
        Remove a trade from the executor tracking.
        """
        self.trade_executor.remove_trade(trade_id)
