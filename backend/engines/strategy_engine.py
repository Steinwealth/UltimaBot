from typing import Dict
from engines.forecast_engine import predict_tp_sl
from engines.confidence_engine import calculate_confidence


def evaluate_trade(symbol: str, market_data: Dict) -> Dict:
    """
    Evaluate a symbol using strategy logic: forecast, confidence, and filters.
    """
    data = market_data.get(symbol, {})
    confidence = calculate_confidence(symbol, data)
    forecast = predict_tp_sl(symbol, data)

    if confidence < 0.95:
        return {"symbol": symbol, "valid": False, "reason": "Low confidence", **forecast}

    if forecast["tp"] <= forecast["sl"]:
        return {"symbol": symbol, "valid": False, "reason": "Unfavorable TP/SL", **forecast}

    return {
        "symbol": symbol,
        "valid": True,
        "confidence": confidence,
        **forecast,
        "reason": "Valid trade"
    }
