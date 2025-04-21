from typing import List

# Simulated symbol pools for crypto and stock
CRYPTO_SYMBOLS = [
    "BTC-USD", "ETH-USD", "SOL-USD", "XRP-USD", "DOGE-USD", "AVAX-USD",
    "MATIC-USD", "SHIB-USD", "LTC-USD", "UNI-USD"
]

STOCK_SYMBOLS = [
    "AAPL", "MSFT", "TSLA", "NVDA", "GOOGL", "META",
    "AMZN", "AMD", "NFLX", "BABA"
]

# Discovery strategies by name (used in crypto mode)
DISCOVERY_STRATEGIES = {
    "original": lambda: CRYPTO_SYMBOLS[:5],
    "volume-spike": lambda: CRYPTO_SYMBOLS[5:8],
    "micro-cap": lambda: CRYPTO_SYMBOLS[8:]
}

def get_symbols(discovery_methods: List[str] = ["original"]) -> List[str]:
    """
    Collects a unique list of tradable symbols based on selected discovery strategies.
    """
    symbols = set()
    for method in discovery_methods:
        if method in DISCOVERY_STRATEGIES:
            symbols.update(DISCOVERY_STRATEGIES[method]())
    return sorted(symbols)

def get_stock_symbols() -> List[str]:
    """
    Returns a static list of premium tradable stock tickers.
    """
    return STOCK_SYMBOLS
