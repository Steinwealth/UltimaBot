# backend/app/api/routes/__init__.py

from .auth import router as auth_router
from .broker import router as broker_router
from .models import router as model_router
from .trades import router as trade_router
from .websocket import router as websocket_router

routers = [
    auth_router,
    broker_router,
    model_router,
    trade_router,
    websocket_router
]

__all__ = [
    "auth_router",
    "broker_router",
    "model_router",
    "trade_router",
    "websocket_router",
    "routers"
]
