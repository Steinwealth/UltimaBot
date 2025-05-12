# backend/app/routers/trading.py

from app.engines.discovery_engine.crypto_discovery import CryptoDiscoveryEngine
from app.engines.strategy_engine.strategy_manager import StrategyManager
from app.engines.forecast_engine.forecast_engine import ForecastEngine
from app.engines.risk_engine.risk_manager import RiskManager
from app.engines.auto_close_engine.auto_close import AutoCloseEngine
from app.engines.trade_tracking.trade_logger import TradeLogger
from app.services.websocket_service import WebSocketService

import asyncio
import httpx


class TradingSystem:
    def __init__(self, broker_client, model, strategy_priority):
        self.broker_client = broker_client
        self.model = model
        self.discovery_engine = CryptoDiscoveryEngine(broker_client)
        self.strategy_manager = StrategyManager(strategy_priority)
        self.forecast_engine = ForecastEngine({"mode": "easy"})
        self.risk_manager = RiskManager()
        self.auto_close_engine = AutoCloseEngine(broker_client)
        self.trade_logger = TradeLogger(db_session=None)  # Inject real session if needed
        self.executed_symbols = set()

    async def safe_broker_call(self, method, *args, retries=5, **kwargs):
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
                    raise e
                await asyncio.sleep(2 ** attempt)

    async def scan_and_trade(self):
        try:
            symbols = await self.discovery_engine.find_symbols()
        except Exception as e:
            await self.trade_logger.log_discovery_error(str(e))
            return

        try:
            account_data = await self.safe_broker_call("get_account_info")
        except Exception as e:
            await self.trade_logger.log_account_error(str(e))
            return

        if not self.risk_manager.check_margin_floor(account_data):
            await self.trade_logger.log_margin_floor(account_data)
            return

        for symbol in symbols:
            if symbol in self.executed_symbols:
                continue

            try:
                forecast = self.forecast_engine.forecast(
                    highs=[1.0] * 20, lows=[0.95] * 20, closes=[0.98] * 20, breakout_velocity=0.03
                )

                if forecast.get("confidence", 0) < 0.95:
                    continue

                available_capital = self.risk_manager.calculate_available_capital(account_data)
                position_size = forecast.get("recommended_size", available_capital / 10)
                if position_size > available_capital:
                    continue

                # Simulate broker trade placement
                entry_price = await self.safe_broker_call("get_price", symbol)
                trade_id = await self.safe_broker_call(
                    "open_trade", symbol=symbol, size=position_size,
                    take_profit=entry_price + forecast["tp"],
                    stop_loss=entry_price - forecast["sl"]
                )

                trade_details = {
                    "trade_id": trade_id,
                    "symbol": symbol,
                    "entry_price": entry_price,
                    "take_profit": entry_price + forecast["tp"],
                    "stop_loss": entry_price - forecast["sl"],
                    "forecast_tp": forecast["tp"],
                    "initial_confidence": forecast["confidence"],
                    "current_confidence": forecast["confidence"],
                    "size": position_size,
                    "entry_time": datetime.utcnow(),
                    "side": "buy",
                    "mode": "easy",
                    "atr": forecast.get("atr", 0.5)
                }

                await self.trade_logger.log_trade_open(trade_details, account_data)

                await WebSocketService.broadcast(
                    broker_id=account_data.get("broker_id", "unknown"),
                    message={"event": "trade_opened", "symbol": symbol}
                )

                self.auto_close_engine.evaluate_trade(trade_details)
                self.executed_symbols.add(symbol)

            except Exception as e:
                await self.trade_logger.log_trade_error(symbol, str(e))

    async def monitor_trades(self):
        try:
            open_trades = await self.safe_broker_call("get_open_trades")
        except Exception as e:
            await self.trade_logger.log_monitor_error("Open Trades Fetch", str(e))
            return

        for trade in open_trades:
            try:
                await self.auto_close_engine.evaluate_trade(trade)
            except Exception as e:
                await self.trade_logger.log_monitor_error(trade.get("symbol", "N/A"), str(e))
