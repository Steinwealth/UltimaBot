from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from models.model_loader import load_model
from engines.discovery_engine import get_symbols
from engines.forecast_engine import predict_tp_sl
from engines.confidence_engine import calculate_confidence
from engines.risk_engine import is_risk_allowed
from engines.strategy_engine import should_trade
from engines.compounding_engine import adjust_position_size
from engines.auto_close_engine import should_exit_trade

router = APIRouter()

class TradeRequest(BaseModel):
    model_name: str
    broker: str
    account_info: dict
    market_data: dict

@router.post("/execute")
def execute_trade(req: TradeRequest):
    model = load_model(req.model_name)
    trade_setups = []

    for symbol in get_symbols():
        if symbol not in req.market_data:
            continue

        price_data = req.market_data[symbol]
        forecast = predict_tp_sl(symbol, price_data)
        confidence = calculate_confidence(symbol, price_data)

        if confidence >= 0.96 and should_trade(symbol, price_data):
            candidate = {
                "symbol": symbol,
                "confidence": confidence,
                "forecast": forecast
            }

            if is_risk_allowed(req.account_info, candidate):
                position_size = adjust_position_size(req.account_info, candidate)
                trade_setups.append({
                    "symbol": symbol,
                    "size": position_size,
                    "tp": forecast["tp"],
                    "sl": forecast["sl"],
                    "confidence": confidence
                })

    if not trade_setups:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="No trades qualified")

    return {
        "model": model.name,
        "trades": trade_setups
    }
