# backend/app/engines/trade_tracking/trade_summary.py

from datetime import datetime
from typing import List, Dict


class TradeSummary:
    def __init__(self):
        self.closed_trades: List[Dict] = []

    async def record_trade_close(self, trade: Dict, close_price: float, exit_reason: str):
        """
        Store a closed trade summary for analytics.
        """
        entry_price = trade.get("entry_price", 0.0)
        size = trade.get("size", 0.0)
        side = trade.get("side", "buy")

        gain = (close_price - entry_price) if side == "buy" else (entry_price - close_price)
        gain_usd = gain * size
        gain_pct = (gain / entry_price) * 100 if entry_price else 0.0

        summary = {
            "symbol": trade["symbol"],
            "trade_id": trade["trade_id"],
            "side": side,
            "entry_price": entry_price,
            "exit_price": close_price,
            "gain_pct": round(gain_pct, 2),
            "gain_usd": round(gain_usd, 2),
            "confidence": round(trade.get("initial_confidence", 0.0), 4),
            "size": size,
            "mode": trade.get("mode"),
            "strategy": trade.get("strategy_id", "N/A"),
            "model": trade.get("model_id", "N/A"),
            "reason": exit_reason,
            "timestamp_opened": trade.get("entry_time"),
            "timestamp_closed": datetime.utcnow()
        }

        self.closed_trades.append(summary)
        return summary

    def get_summary(self) -> List[Dict]:
        """
        Returns the list of all closed trade summaries.
        """
        return self.closed_trades

    def reset(self):
        """
        Clears all recorded summaries.
        """
        self.closed_trades.clear()
