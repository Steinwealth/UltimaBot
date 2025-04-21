# backend/engines/auto_close_engine.py

from typing import Dict

def should_close_trade(
    current_price: float,
    entry_price: float,
    forecast_tp: float,
    forecast_sl: float,
    confidence: float,
    trailing_triggered: bool,
    price_high_since_entry: float,
    volatility_30m: float,
    avg_volatility_30m: float,
    mode: str = "hard",
    max_drawdown_pct: float = 0.07
) -> Dict:
    """
    Determine if a trade should auto-close based on dynamic logic, including:
    - Confidence drop
    - Reversal near TP zone
    - Volatility reversal protection
    - Dynamic trailing SL logic post-TP
    """
    price_change_pct = (current_price - entry_price) / entry_price
    confidence_drop = confidence < 0.93
    tp_zone_reversal = price_change_pct > 0.9 * forecast_tp and trailing_triggered
    drawdown_trigger = price_change_pct <= -max_drawdown_pct

    # Volatility Reversal Protection (Easy Mode priority)
    volatility_reversal = (
        volatility_30m > avg_volatility_30m * 1.5 and price_change_pct < -0.03
    ) if mode == "easy" else False

    # Trailing SL Logic Above TP (Hard Mode priority)
    trailing_tp_sl_trigger = (
        price_high_since_entry > forecast_tp * 1.05 and current_price < price_high_since_entry * 0.975
    ) if mode == "hard" else False

    should_close = (
        confidence_drop or tp_zone_reversal or drawdown_trigger or
        volatility_reversal or trailing_tp_sl_trigger
    )

    return {
        "should_close": should_close,
        "confidence_drop": confidence_drop,
        "tp_zone_reversal": tp_zone_reversal,
        "drawdown_trigger": drawdown_trigger,
        "volatility_reversal": volatility_reversal,
        "trailing_tp_sl_trigger": trailing_tp_sl_trigger,
        "price_change_pct": round(price_change_pct * 100, 2)
    }
