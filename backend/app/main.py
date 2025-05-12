# backend/app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import (
    broker as broker_routes,
    trades as trade_routes,
    models as model_routes,
    websocket as websocket_routes
)
from app.utils.database import connect_db
from app.utils.market_data import initialize_market_feeds
from app.engines.trading_loop import run_trading_cycle
from app.core.scheduler import start_scheduler
import asyncio
import logging
import os

# -------------------------
# App Initialization
# -------------------------
app = FastAPI(
    title="Ultima Bot API",
    version="1.0.0",
    description="AI-powered multi-broker crypto & stock trading backend"
)

# -------------------------
# CORS Configuration
# -------------------------
origins = [
    "http://localhost:3000",
    "http://localhost:5173",
    "https://ultima-bot-frontend.com",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------
# Route Registration
# -------------------------
app.include_router(broker_routes.router, prefix="/api/brokers", tags=["Brokers"])
app.include_router(trade_routes.router, prefix="/api/trades", tags=["Trades"])
app.include_router(model_routes.router, prefix="/api/models", tags=["Models"])
app.include_router(websocket_routes.router, tags=["WebSocket"])

# -------------------------
# Startup Lifecycle Hook
# -------------------------
@app.on_event("startup")
async def startup_event():
    logging.basicConfig(level=logging.INFO)
    logging.info("🚀 Ultima Bot backend starting...")

    await connect_db()
    await initialize_market_feeds()
    start_scheduler()  # ⏰ Launch scheduler tasks
    asyncio.create_task(run_trading_cycle())

    logging.info("✅ Ultima Bot backend initialized and running.")

# -------------------------
# Entrypoint for Uvicorn
# -------------------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8000)),
        reload=bool(os.getenv("RELOAD", "False") == "True")
    )
