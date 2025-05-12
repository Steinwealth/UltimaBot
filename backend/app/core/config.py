# backend/app/core/config.py

import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    API_V1_STR: str = "/api"
    PROJECT_NAME: str = "Ultima Bot"

    # Broker API Keys
    COINBASE_API_KEY: str = os.getenv("COINBASE_API_KEY", "")
    COINBASE_API_SECRET: str = os.getenv("COINBASE_API_SECRET", "")
    BINANCE_API_KEY: str = os.getenv("BINANCE_API_KEY", "")
    BINANCE_API_SECRET: str = os.getenv("BINANCE_API_SECRET", "")
    KRAKEN_API_KEY: str = os.getenv("KRAKEN_API_KEY", "")
    KRAKEN_API_SECRET: str = os.getenv("KRAKEN_API_SECRET", "")
    ETRADE_API_KEY: str = os.getenv("ETRADE_API_KEY", "")
    ETRADE_API_SECRET: str = os.getenv("ETRADE_API_SECRET", "")
    ETRADE_OAUTH_TOKEN: str = os.getenv("ETRADE_OAUTH_TOKEN", "")
    ETRADE_OAUTH_SECRET: str = os.getenv("ETRADE_OAUTH_SECRET", "")
    BITFINEX_API_KEY: str = os.getenv("BITFINEX_API_KEY", "")
    BITFINEX_API_SECRET: str = os.getenv("BITFINEX_API_SECRET", "")
    INTERACTIVE_BROKERS_KEY: str = os.getenv("IB_API_KEY", "")
    INTERACTIVE_BROKERS_ACCOUNT: str = os.getenv("IB_ACCOUNT_ID", "")

    # DeFi Wallet RPC URLs (Polygon by default)
    METAMASK_RPC_URL: str = os.getenv("METAMASK_RPC_URL", "https://polygon-rpc.com")
    TRUSTWALLET_RPC_URL: str = os.getenv("TRUSTWALLET_RPC_URL", "https://polygon-rpc.com")
    COINBASEWALLET_RPC_URL: str = os.getenv("COINBASEWALLET_RPC_URL", "https://polygon-rpc.com")

    # WebSocket and Redis
    WEBSOCKET_BROKER_CHANNEL: str = "broker_updates"
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379")

    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://postgres:password@db:5432/ultima")

    class Config:
        case_sensitive = True


# Instantiate settings globally
settings = Settings()
