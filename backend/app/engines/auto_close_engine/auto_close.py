# backend/app/engines/auto_close_engine/auto_close.py

from datetime import datetime
from typing import Dict, Any
from app.services.broadcast_service import BroadcastService
from app.engines.trade_tracking.trade_summary import TradeSummary


class AutoCloseEngine:
    def __init__(
        self,
        broker_client,
        confidence_floor: float = 0.93,
        confidence_drop_threshold: float = 0.10,
        hero_mode_close_time: int = 60,
        trail_to_moon_buffer: float = 0.95,
        momentum_buffer: float = 0.02,
    ):
        self.broker_client = broker_client
        self.confidence_floor = confidence_floor
        self.confidence_drop_threshold = confidence_drop_threshold
        self.hero_mode_close_time = hero_mode_close_time
        self.trail_to_moon_buffer = trail_to_moon_buffer
        self.momentum_buffer = momentum_buffer

    async def evaluate_trade(self, trade: Dict[str, Any]):
        current_price = await self.broker_client.get_price(trade['symbol'])

        if await self._check_tp_sl(trade, current_price):
            return

        if trade.get('forecast_tp'):
            await self._trail_to_moon(trade, current_price)

        if self._confidence_exit(trade, current_price):
            await self._close_and_broadcast(trade, current_price, "confidence_exit")
            return

        if self._hero_mode_exit(trade, current_price):
            await self._close_and_broadcast(trade, current_price, "hero_mode_timeout")

    async def _check_tp_sl(self, trade: Dict[str, Any], current_price: float) -> bool:
        tp, sl = trade['take_profit'], trade['stop_loss']
        side = trade['side']

        if side == 'buy':
            if current_price >= tp:
                await self._close_and_broadcast(trade, current_price, "take_profit")
                return True
            elif current_price <= sl:
                await self._close_and_broadcast(trade, current_price, "stop_loss")
                return True
        elif side == 'sell':
            if current_price <= tp:
                await self._close_and_broadcast(trade, current_price, "take_profit")
                return True
            elif current_price >= sl:
                await self._close_and_broadcast(trade, current_price, "stop_loss")
                return True
        return False

    async def _trail_to_moon(self, trade: Dict[str, Any], current_price: float):
        activation_price = trade['forecast_tp'] * self.trail_to_moon_buffer
        if current_price >= activation_price:
            atr = trade.get('atr', 0.5)
            trail_distance = atr * 0.6
            await self._apply_trailing_stop(trade, current_price, trail_distance)

    async def _apply_trailing_stop(self, trade: Dict[str, Any], current_price: float, trail_distance: float):
        side = trade['side']
        new_stop = current_price - trail_distance if side == 'buy' else current_price + trail_distance
        if (side == 'buy' and new_stop > trade['stop_loss']) or (side == 'sell' and new_stop < trade['stop_loss']):
            trade['stop_loss'] = new_stop
            await self.broker_client.update_trade(trade['trade_id'], trade)

    def _confidence_exit(self, trade: Dict[str, Any], current_price: float) -> bool:
        initial = trade.get('initial_confidence', 1.0)
        current = trade.get('current_confidence', 1.0)

        if initial == 0:
            return False

        drop_pct = (initial - current) / initial
        below_floor = current < self.confidence_floor
        is_profitable = current_price > trade['entry_price'] if trade['side'] == 'buy' else current_price < trade['entry_price']
        has_momentum = self._check_price_momentum(trade, current_price)

        return (below_floor or drop_pct >= self.confidence_drop_threshold) and is_profitable and not has_momentum

    def _check_price_momentum(self, trade: Dict[str, Any], current_price: float) -> bool:
        last_prices = trade.get('recent_prices', [])
        if len(last_prices) < 3:
            return False
        momentum = (current_price - last_prices[-3]) / last_prices[-3]
        return momentum > self.momentum_buffer

    def _hero_mode_exit(self, trade: Dict[str, Any], current_price: float) -> bool:
        if trade.get('mode') != 'Hero':
            return False

        elapsed = (datetime.utcnow() - trade['entry_time']).total_seconds() / 60
        is_profitable = current_price > trade['entry_price'] if trade['side'] == 'buy' else current_price < trade['entry_price']
        return elapsed >= self.hero_mode_close_time and is_profitable

    async def _close_and_broadcast(self, trade: Dict[str, Any], price: float, reason: str):
        await self.broker_client.close_trade(trade['trade_id'], reason=reason)

        gain = (price - trade['entry_price']) if trade['side'] == 'buy' else (trade['entry_price'] - price)
        gain_pct = (gain / trade['entry_price']) * 100
        gain_usd = gain_pct * (trade['size'] / 100)

        await BroadcastService.trade_close(
            symbol=trade['symbol'],
            gain_pct=round(gain_pct, 2),
            gain_usd=round(gain_usd, 2),
            rationale=reason
        )

        await TradeSummary().record_trade_close({
            "symbol": trade['symbol'],
            "trade_id": trade['trade_id'],
            "mode": trade.get("mode"),
            "model_id": trade.get("model_id"),
            "strategy_id": trade.get("strategy_id"),
            "confidence": trade.get("initial_confidence"),
            "size": trade.get("size"),
            "entry_price": trade['entry_price'],
            "exit_price": price,
            "gain_pct": gain_pct,
            "gain_usd": gain_usd,
            "exit_reason": reason,
            "timestamp": datetime.utcnow().isoformat()
        })
