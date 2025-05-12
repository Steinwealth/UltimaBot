# backend/app/services/discovery_service.py

from app.engines.discovery_engine.crypto_discovery import CryptoDiscoveryEngine
from app.engines.discovery_engine.stock_discovery import StockDiscoveryEngine
from typing import Dict, List


class DiscoveryService:
    def __init__(self, broker_client, market_type: str = "crypto"):
        self.market_type = market_type.lower()
        self.broker_client = broker_client
        self.crypto_engine = None
        self.stock_engine = None

        if self.market_type == "crypto":
            self.crypto_engine = CryptoDiscoveryEngine(broker_client=self.broker_client)
        elif self.market_type == "stock":
            self.stock_engine = StockDiscoveryEngine(broker_client=self.broker_client, strategy="top_volume")

    async def discover_all_symbols(self) -> Dict[str, List[str]]:
        """
        Run both crypto and stock discovery engines (if both are initialized).
        """
        crypto = await self.crypto_engine.find_symbols() if self.crypto_engine else []
        stock = await self.stock_engine.find_symbols() if self.stock_engine else []
        return {
            "crypto": crypto,
            "stock": stock
        }

    async def discover_crypto(self) -> List[str]:
        if not self.crypto_engine:
            raise ValueError("Crypto Discovery Engine is not initialized.")
        return await self.crypto_engine.find_symbols()

    async def discover_stock(self) -> List[str]:
        if not self.stock_engine:
            raise ValueError("Stock Discovery Engine is not initialized.")
        return await self.stock_engine.find_symbols()
