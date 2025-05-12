# backend/app/services/trade_executor_service.py

from datetime import datetime
from typing import Dict, Any
import asyncio
import httpx

from app.engines.execution_engine.trade_executor import TradeExecutor
from app.engines.auto_close_engine.auto_close import AutoCloseEngine
from app.engines.risk_engine.risk_manager import RiskManager
from app.engines.trade_tracking.trade_logger import TradeLogger
from app.services.websocket_service import WebSocketService


class TradeExecutorService:
    def __init__(self, broker_client, model, db_session):
        self.broker_client = broker_client
        self.model = model
        self.db_session = db_session

        self.risk_manager = RiskManager()
        self.trade_logger = TradeLogger(db_session)
        self.auto_close_engine = AutoCloseEngine(broker_client)

    async def safe_broker_call(self, method: str, *args, retries: int = 5, **kwargs):
        """
        Handles rate limits (HTTP 429) and retries broker API calls.
        """
        for attempt in range(retries):
            try:
                return await getattr(self.broker_client, method)(*args, **kwargs)
            except httpx.HTTPStatusError as e:
                if e.response.status_code == 429:
                    await asyncio.sleep(2 ** attempt)
                else:
                    raise
            except Exception as e:
                if attempt == retries - 1:
                    raise
                await asyncio.sleep(2 ** attempt)

    async def execute_manual_trade(
        self,
        symbol: str,
        forecast: Dict[str, Any],
        account_data: Dict[str, Any],
        mode: str = "Easy",
        model_id: str = None,
        strategy_id: str = None,
    ) -> Dict[str, Any]:
        """
        Executes a trade manually using provided forecast and account data.
        Used for manual endpoints or model-controlled batch triggers.
        """
        required_fields = ['tp', 'sl', 'confidence']
        for field in required_fields:
            if field not in forecast:
                raise ValueError(f"Forecast missing required field: {field}")

        # Step 1: Capital and position sizing
        available_capital = self.risk_manager.calculate_available_capital(account_data)
        position_size = forecast.get("recommended_size", available_capital * 0.1)
        if position_size > available_capital:
            raise ValueError("Position size exceeds available capital")

        # Step 2: Get entry price safely
        entry_price = await self.safe_broker_call("get_price", symbol)

        # Step 3: Place order
        trade_id = await self.safe_broker_call(
            "place_order",
            symbol=symbol,
            position_size=position_size,
            trade_type="buy"
        )

        # Step 4: Build trade object
        trade_details = {
            "trade_id": trade_id,
            "symbol": symbol,
            "side": "buy",
            "entry_price": entry_price,
            "take_profit": forecast["tp"],
            "stop_loss": forecast["sl"],
            "forecast_tp": forecast["tp"],
            "atr": forecast.get("atr", 0.5),
            "initial_confidence": forecast["confidence"],
            "current_confidence": forecast["confidence"],
            "entry_time": datetime.utcnow(),
            "mode": mode,
            "model_id": model_id,
            "strategy_id": strategy_id,
            "size": position_size,
            "broker_id": account_data.get("broker_id", "unknown"),
        }

        # Step 5: Log the trade
        await self.trade_logger.log_trade_open(trade_details, account_data)

        # Step 6: Broadcast opening
        await WebSocketService.broadcast(
            broker_id=trade_details["broker_id"],
            message={
                "event": "trade_opened",
                "symbol": symbol,
                "trade_id": trade_id,
                "entry_price": entry_price,
                "size": position_size,
                "confidence": forecast["confidence"],
                "tp": forecast["tp"],
                "sl": forecast["sl"],
            }
        )

        # Step 7: Attach to AutoClose monitoring
        await self.auto_close_engine.evaluate_trade(trade_details)  # initial evaluation

        return {"status": "Trade executed", "trade_id": trade_id}
