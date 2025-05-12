# backend/app/api/routes/trades.py

from fastapi import APIRouter, HTTPException
from app.services.trade_service import TradeService

router = APIRouter()

@router.get("/trades/{broker_id}")
async def list_trades(broker_id: str):
    """
    List all trades for a broker account.
    """
    try:
        return await TradeService.get_trades_for_broker(broker_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/trades/{broker_id}/execute")
async def execute_trade(broker_id: str, symbol: str, quantity: float, side: str):
    """
    Execute a trade (buy/sell) on a broker account.
    """
    try:
        return await TradeService.execute_trade(broker_id, symbol, quantity, side)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/trades/{broker_id}/close")
async def close_trade(broker_id: str, trade_id: str):
    """
    Close an open trade.
    """
    try:
        return await TradeService.close_trade(broker_id, trade_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
