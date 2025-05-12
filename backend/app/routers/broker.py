# backend/app/routers/broker.py

from fastapi import APIRouter, HTTPException, Header
from pydantic import BaseModel
from typing import Dict, List, Optional
from app.utils.broker_clients import BrokerManager

router = APIRouter()

# In-memory session state
active_broker_sessions: Dict[str, Dict[str, bool]] = {}

class BrokerLogin(BaseModel):
    broker: str
    api_key: Optional[str] = None
    api_secret: Optional[str] = None
    polygon_key: Optional[str] = None
    wallet_address: Optional[str] = None  # For DeFi wallets
    rpc_url: Optional[str] = None         # Optional override for RPC

class BrokerStatus(BaseModel):
    broker: str
    account_id: str
    balance: float
    buying_power: float
    cash_available: float
    margin_balance: float
    margin_used: float
    margin_enabled: bool
    margin_percent: float
    status: str

class DisconnectRequest(BaseModel):
    broker: str

class ActiveBrokerResponse(BaseModel):
    brokers: List[str]

# ------------------------
# Broker Login
# ------------------------
@router.post("/login", response_model=BrokerStatus)
async def login_broker(credentials: BrokerLogin, authorization: str = Header(default="")):
    broker_client = BrokerManager.get_client(credentials.broker)
    if not broker_client:
        raise HTTPException(status_code=400, detail="Unsupported broker")

    # DeFi wallet support (MetaMask, Trust Wallet, etc.)
    if credentials.broker.lower() == "metamask":
        if not credentials.wallet_address:
            raise HTTPException(status_code=400, detail="Wallet address is required for MetaMask")
        await broker_client.login(wallet_address=credentials.wallet_address, rpc_url=credentials.rpc_url)
    else:
        # Centralized exchange login (Coinbase, Kraken, etc.)
        account_info = await broker_client.login(
            api_key=credentials.api_key,
            api_secret=credentials.api_secret,
            polygon_key=credentials.polygon_key
        )
        if not account_info:
            raise HTTPException(status_code=401, detail="Login failed")

    token = authorization.replace("Bearer ", "") or "public"
    active_broker_sessions.setdefault(token, {})[credentials.broker] = True

    account_info = await broker_client.get_account_info()

    return BrokerStatus(
        broker=credentials.broker,
        account_id=account_info["account_id"],
        balance=account_info["balance"],
        buying_power=account_info.get("buying_power", account_info["balance"]),
        cash_available=account_info.get("cash_available", account_info["balance"]),
        margin_balance=account_info.get("margin_balance", 0.0),
        margin_used=account_info.get("margin_used", 0.0),
        margin_enabled=account_info.get("margin_enabled", False),
        margin_percent=account_info.get("margin_percent", 0.0),
        status="Connected"
    )

# ------------------------
# Broker Status
# ------------------------
@router.get("/status/{broker}", response_model=BrokerStatus)
async def broker_status(broker: str):
    broker_client = BrokerManager.get_client(broker)
    if not broker_client or not broker_client.is_logged_in():
        raise HTTPException(status_code=404, detail="Broker not connected")

    account_info = await broker_client.get_account_info()
    return BrokerStatus(
        broker=broker,
        account_id=account_info["account_id"],
        balance=account_info["balance"],
        buying_power=account_info.get("buying_power", account_info["balance"]),
        cash_available=account_info.get("cash_available", account_info["balance"]),
        margin_balance=account_info.get("margin_balance", 0.0),
        margin_used=account_info.get("margin_used", 0.0),
        margin_enabled=account_info.get("margin_enabled", False),
        margin_percent=account_info.get("margin_percent", 0.0),
        status="Connected"
    )

# ------------------------
# Disconnect Broker
# ------------------------
@router.post("/disconnect")
async def disconnect_broker(req: DisconnectRequest, authorization: str = Header(default="")):
    token = authorization.replace("Bearer ", "") or "public"
    broker_id = req.broker

    if token not in active_broker_sessions or broker_id not in active_broker_sessions[token]:
        raise HTTPException(status_code=404, detail="Broker not found")

    broker_client = BrokerManager.get_client(broker_id)
    if broker_client and broker_client.is_logged_in():
        await broker_client.logout()

    del active_broker_sessions[token][broker_id]
    return {"status": "disconnected", "broker": broker_id}

# ------------------------
# List Active Brokers
# ------------------------
@router.get("/brokers/active", response_model=ActiveBrokerResponse)
async def get_active_brokers(authorization: str = Header(default="")):
    token = authorization.replace("Bearer ", "") or "public"
    brokers = list(active_broker_sessions.get(token, {}).keys())
    return {"brokers": brokers}
