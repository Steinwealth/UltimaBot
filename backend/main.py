from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from backend.routers import brokers, trades, models
from backend.utils.database import connect_db
from backend.utils.market_data import initialize_market_feeds
from backend.engines.trade_executor import TradeExecutor
from backend.engines.trading_loop import run_trading_cycle
import asyncio

app = FastAPI()

# Allow CORS for frontend communication
origins = [
    "http://localhost:3000",
    "https://ultima-bot-frontend.com",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(brokers.router, prefix="/api/brokers", tags=["Brokers"])
app.include_router(trades.router, prefix="/api/trades", tags=["Trades"])
app.include_router(models.router, prefix="/api/models", tags=["Models"])

# Initialize database, market feeds, TradeExecutor, and start the trading loop
@app.on_event("startup")
async def startup_event():
    await connect_db()
    await initialize_market_feeds()
    TradeExecutor.initialize()  # Singleton initialization
    asyncio.create_task(run_trading_cycle())  # Background trading loop

# WebSocket for live trade updates
active_connections = []

@app.websocket("/ws/trades")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    active_connections.append(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            # Handle incoming WebSocket messages (e.g., commands)
            await websocket.send_text(f"Command received: {data}")
    except Exception as e:
        print(f"WebSocket error: {e}")
    finally:
        active_connections.remove(websocket)

# Function to broadcast live trade updates to all WebSocket clients
async def broadcast_trade_update(update):
    for connection in active_connections:
        await connection.send_json({"type": "trade_update", "data": update})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
