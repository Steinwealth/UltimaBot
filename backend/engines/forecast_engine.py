from typing import Dict
import random

# Simulate forecast TP/SL using basic market stats

def predict_tp_sl(symbol: str, price_data: Dict) -> Dict:
    """
    Simulate TP/SL prediction using volatility, trend, and confidence factors.
    """
    atr = price_data.get("atr", 0.02)
    confidence = price_data.get("confidence", 0.95)
    trend_strength = price_data.get("trend_strength", 1.0)

    base_tp = atr * random.uniform(2.5, 4.5)
    base_sl = atr * random.uniform(0.8, 1.6)

    # Adjust TP upward if trend and confidence are strong
    tp = base_tp * (1 + (confidence - 0.9) * 2 + trend_strength * 0.3)
    sl = base_sl * (1 - (confidence - 0.9) * 0.5)

    return {
        "tp": round(tp, 4),
        "sl": round(sl, 4),
        "confidence": round(confidence, 3),
        "trend_strength": trend_strength
    }
