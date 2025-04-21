# backend/routers/auth.py

from fastapi import APIRouter, HTTPException, status, Request
from pydantic import BaseModel
import os

router = APIRouter()

class BrokerAuthRequest(BaseModel):
    broker: str
    api_key: str
    api_secret: str
    polygon_key: str = None

SUPPORTED_BROKERS = [
    "coinbase",
    "etrade",
    "robinhood",
    "binance",
    "interactive_brokers",
    "gemini",
    "kraken",
    "tastytrade",
    "charles_schwab",
    "fidelity",
    "td_ameritrade"
]

@router.post("/login")
def login(request: BrokerAuthRequest):
    # Broker validation
    if request.broker.lower() not in SUPPORTED_BROKERS:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Unsupported broker")

    # Store credentials (use secure storage in production)
    os.environ[f"{request.broker.upper()}_API_KEY"] = request.api_key
    os.environ[f"{request.broker.upper()}_API_SECRET"] = request.api_secret
    if request.polygon_key:
        os.environ["POLYGON_KEY"] = request.polygon_key

    return {
        "message": f"Login successful for broker: {request.broker.title()}"
    }
