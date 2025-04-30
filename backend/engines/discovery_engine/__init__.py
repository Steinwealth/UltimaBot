# backend/engines/discovery_engine/__init__.py

from .crypto_discovery import CryptoDiscoveryEngine
from .stock_discovery import StockDiscoveryEngine

# Expose the engines when importing the package
__all__ = [
    "CryptoDiscoveryEngine",
    "StockDiscoveryEngine"
]
