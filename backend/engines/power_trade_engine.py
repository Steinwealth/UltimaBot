from typing import Dict, List
from engines.forecast_engine import predict_tp_sl
from engines.confidence_engine import calculate_confidence
from engines.compounding_engine import calculate_position_size
from engines.power_trade_engine import classify_power_trade


def evaluate_trade(
    symbol: str,
    market_data: Dict,
    balance: float,
    win_streak: int,
    available_margin_pct: float,
    base_risk_pct: float = 0.01,
    use_loss_recovery: bool = False,
    last_trade_was_loss: bool = False
) -> Dict:
    """
    Evaluate a single trade with forecast, confidence, power tier, and compounding logic.
    """
    data = market_data.get(symbol, {})
    confidence = calculate_confidence(symbol, data)
    forecast = predict_tp_sl(symbol, data)

    if confidence < 0.95:
        return {"symbol": symbol, "valid": False, "reason": "Low confidence", **forecast}

    if forecast["tp"] <= forecast["sl"]:
        return {"symbol": symbol, "valid": False, "reason": "Unfavorable TP/SL", **forecast}

    power_trade = classify_power_trade(confidence, available_margin_pct)
    position_size = calculate_position_size(
        balance,
        base_risk_pct,
        win_streak,
        use_loss_recovery=use_loss_recovery,
        last_trade_was_loss=last_trade_was_loss,
        power_tier=power_trade["tier"]
    )

    return {
        "symbol": symbol,
        "valid": True,
        "confidence": confidence,
        **forecast,
        "position_size": position_size,
        "power_trade_tier": power_trade["tier"],
        "reason": "Valid trade"
    }


def evaluate_trades(
    symbols: List[str],
    market_data: Dict,
    balance: float,
    win_streak: int,
    available_margin_pct: float,
    base_risk_pct: float = 0.01,
    use_loss_recovery: bool = False,
    last_trade_was_loss: bool = False
) -> List[Dict]:
    """
    Evaluate multiple trades using batch logic.
    """
    results = []
    for symbol in symbols:
        result = evaluate_trade(
            symbol,
            market_data,
            balance,
            win_streak,
            available_margin_pct,
            base_risk_pct,
            use_loss_recovery,
            last_trade_was_loss
        )
        results.append(result)
    return results
