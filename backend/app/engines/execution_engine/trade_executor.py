# backend/engines/execution_engine/trade_executor.py

from datetime import datetime
from typing import Dict, Any
import asyncio

from app.services.websocket_service import WebSocketService
from app.engines.trade_tracking.trade_summary import TradeSummary
from app.engines.trade_tracking.trade_logger import TradeLogger
from app.db.database import SessionLocal

class TradeExecutor:
    def __init__(self, broker_client, risk_manager, strategy_manager, forecast_engine):
        self.broker_client = broker_client
        self.risk_manager = risk_manager
        self.strategy_manager = strategy_manager
        self.forecast_engine = forecast_engine
        self.open_trades: Dict[str, Dict[str, Any]] = {}
        self.win_streak: Dict[str, int] = {}
        self.trade_summary = TradeSummary()
        self.trade_logger = TradeLogger(SessionLocal())

    async def execute_trade(self, symbol: str, market_data: Dict[str, Any], account_data: Dict[str, Any], mode_settings: Dict[str, Any]) -> str:
        try:
            price = market_data['price']
            highs = market_data['highs']
            lows = market_data['lows']
            closes = market_data['closes']
            velocity = market_data.get('velocity', 0)
            win_streak = market_data.get('win_streak', 0)

            forecast = self.forecast_engine.forecast(highs, lows, closes, velocity)
            confidence = forecast.get('confidence', 0)
            tp = forecast.get('tp')
            sl = forecast.get('sl')
            atr = self.forecast_engine.calculate_atr(highs, lows, closes)

            if not self.risk_manager.check_volatility_filter(atr, price):
                return "volatility_filtered"
            if confidence < 0.95:
                return "confidence_too_low"
            if not self.risk_manager.check_margin_floor(account_data):
                return "margin_floor_breach"

            available_capital = self.risk_manager.calculate_available_capital(account_data)
            power_tier = self.risk_manager.get_power_trade_tier(confidence)
            multiplier = self.risk_manager.get_scaling_multiplier(power_tier, win_streak)
            base_size = available_capital * 0.02
            position_size = base_size * multiplier

            if not self.risk_manager.check_trade_risk(position_size, account_data['balance']):
                return "trade_risk_limit"

            trade = {
                "symbol": symbol,
                "entry_price": price,
                "take_profit": price + tp,
                "stop_loss": price - sl,
                "forecast_tp": price + tp,
                "initial_confidence": confidence,
                "current_confidence": confidence,
                "side": "buy",
                "size": position_size,
                "entry_time": datetime.utcnow(),
                "mode": mode_settings.get("mode", "easy"),
                "recent_prices": closes[-3:] if len(closes) >= 3 else closes,
                "atr": atr,
                "trailing_anchor": forecast.get("trailing_anchor", 0.75),
                "broker_id": account_data.get("broker_id", "unknown"),
                "model_id": account_data.get("model_id"),
                "strategy_id": market_data.get("strategy_id")
            }

            trade_id = await self.broker_client.open_trade(
                symbol=symbol,
                size=position_size,
                take_profit=trade["take_profit"],
                stop_loss=trade["stop_loss"]
            )

            if trade_id:
                trade["trade_id"] = trade_id
                self.open_trades[trade_id] = trade

                await self.trade_logger.log_trade_open(trade, account_data)

                await WebSocketService.broadcast(
                    broker_id=trade["broker_id"],
                    message={
                        "event": "trade_opened",
                        "symbol": symbol,
                        "trade_id": trade_id,
                        "entry_price": trade["entry_price"],
                        "size": trade["size"],
                        "confidence": confidence,
                        "tp": trade["take_profit"],
                        "sl": trade["stop_loss"],
                    }
                )
                return "trade_opened"
            else:
                return "broker_error"

        except Exception as e:
            print(f"[TradeExecutor] Error executing trade for {symbol}: {e}")
            return "execution_error"

    def get_open_trades(self) -> Dict[str, Any]:
        return self.open_trades

    def remove_trade(self, trade_id: str, result: Dict[str, Any] = None):
        trade = self.open_trades.pop(trade_id, None)
        if not trade:
            return

        broker_id = trade.get("broker_id", "unknown")
        gain_pct = result.get("gain_pct", 0) if result else 0
        gain_usd = result.get("gain_usd", 0) if result else 0
        reason = result.get("reason", "manual_close")

        trade["exit_price"] = trade["entry_price"] + (gain_usd * 100 / trade["size"]) if trade["side"] == "buy" else trade["entry_price"] - (gain_usd * 100 / trade["size"])

        # ✅ Win streak tracking
        if gain_pct > 0:
            self.win_streak[broker_id] = self.win_streak.get(broker_id, 0) + 1
        else:
            self.win_streak[broker_id] = 0

        # ✅ Win streak marquee celebration
        streak = self.win_streak[broker_id]
        streak_messages = {
            10: "Winning Streak for 10 Trades!",
            15: "Brutality!!!",
            20: "Tubular!!!",
            25: "Explosive!!!",
            30: "Groovy!!!",
            35: "€£$¥!!!",
        }
        if streak in streak_messages:
            asyncio.create_task(WebSocketService.broadcast(
                broker_id=broker_id,
                message={
                    "event": "win_streak",
                    "streak": streak,
                    "text": streak_messages[streak],
                    "sound": "win_streak.mp3"
                }
            ))

        # ✅ Close trade summary + log
        close_text = f"{trade['symbol']} closed {gain_pct:+.1f}% (${gain_usd:+.2f}) — {reason}"
        asyncio.create_task(WebSocketService.broadcast(
            broker_id=broker_id,
            message={
                "event": "trade_closed",
                "symbol": trade["symbol"],
                "trade_id": trade_id,
                "exit_time": datetime.utcnow().isoformat(),
                "text": close_text,
                "sound": "negative.mp3" if gain_pct < 0 else None
            }
        ))

        # ✅ Log to DB + Summary
        asyncio.create_task(self.trade_logger.log_trade_close(trade, reason, trade["exit_price"]))
        asyncio.create_task(self.trade_summary.record_trade_close({
            "symbol": trade["symbol"],
            "trade_id": trade_id,
            "mode": trade.get("mode"),
            "model_id": trade.get("model_id"),
            "strategy_id": trade.get("strategy_id"),
            "confidence": trade.get("initial_confidence"),
            "size": trade.get("size"),
            "entry_price": trade["entry_price"],
            "exit_price": trade["exit_price"],
            "gain_pct": gain_pct,
            "gain_usd": gain_usd,
            "exit_reason": reason,
            "timestamp": datetime.utcnow().isoformat()
        }))
