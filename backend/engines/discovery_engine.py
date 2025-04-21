from typing import List, Tuple
from engines.confidence_engine import calculate_confidence
import random
from datetime import datetime, timedelta

# === Symbol pools (for simulation/demo) ===
CRYPTO_SYMBOLS = [
    "BTC-USD", "ETH-USD", "SOL-USD", "XRP-USD", "DOGE-USD", "AVAX-USD",
    "MATIC-USD", "SHIB-USD", "LTC-USD", "UNI-USD"
]

STOCK_SYMBOLS = [
    "AAPL", "MSFT", "TSLA", "NVDA", "GOOGL", "META",
    "AMZN", "AMD", "NFLX", "BABA",
    "TQQQ", "5QQQ", "SOXL", "SPYU", "SPXL", "MSTX", "BITX", "SHNY", "UGL", "DGP",
    "QQQM", "SPY", "GLDM"
]

# Crypto discovery logic
DISCOVERY_STRATEGIES = {
    "original": lambda: CRYPTO_SYMBOLS[:5],
    "volume-spike": lambda: CRYPTO_SYMBOLS[5:8],
    "micro-cap": lambda: CRYPTO_SYMBOLS[8:]
}

def get_symbols(discovery_methods: List[str] = ["original"]) -> List[str]:
    symbols = set()
    for method in discovery_methods:
        if method in DISCOVERY_STRATEGIES:
            symbols.update(DISCOVERY_STRATEGIES[method]())
    return sorted(symbols)

def get_stock_symbols() -> List[str]:
    return STOCK_SYMBOLS

# === STOCK STRATEGY FILTERS ===

def ultima_strategy(market_data: dict) -> List[str]:
    result = []
    for symbol, data in market_data.items():
        if (
            data.get("rsi", 0) >= 50 and
            data.get("macd", 0) > 0 and
            data.get("volume_surge", 0) > 1.5 and
            data.get("atr", 10) <= 2.8 and
            calculate_confidence(symbol, data) >= 0.75
        ):
            result.append(symbol)
    for etf in ["QQQM", "SPY", "GLDM"]:
        if etf in market_data:
            d = market_data[etf]
            if d.get("rsi", 0) >= 50 and d.get("macd", 0) > 0:
                result.append(etf)
    return result

def freshman_strategy(market_data: dict) -> List[str]:
    result = []
    for symbol, data in market_data.items():
        if (
            1 <= data.get("price", 0) <= 10 and
            data.get("relative_volume", 0) > 5 and
            data.get("volume", 0) > 100_000 and
            data.get("float", 100_000_000) < 20_000_000
        ):
            result.append(symbol)
    return result

def top_volume_strategy(market_data: dict) -> List[str]:
    result = []
    for symbol, data in market_data.items():
        if (
            data.get("volume_rank", 999) <= 50 and
            data.get("volume", 0) >= data.get("avg_volume", 1) * 2 and
            data.get("rsi", 0) >= 50 and
            data.get("macd_recent_cross", False) and
            data.get("atr", 10) <= 3.0 and
            data.get("price", 0) >= 2
        ):
            result.append(symbol)
    return result

def super_leverage_strategy(market_data: dict) -> List[str]:
    symbols = ["TQQQ", "5QQQ", "SOXL", "SPYU", "SPXL", "MSTX", "BITX", "SHNY", "UGL", "DGP"]
    result = []
    for symbol in symbols:
        data = market_data.get(symbol, {})
        if (
            data.get("volume_1min", 0) > data.get("avg_volume_1min", 1) * 1.3 and
            data.get("rsi", 0) >= 55 and
            data.get("macd_recent_cross", False) and
            data.get("atr", 0) > 2.5 and
            data.get("volatility_30min", 0) >= 3.0
        ):
            result.append(symbol)
    return result

def large_cap_strategy(market_data: dict) -> List[str]:
    result = []
    for symbol, data in market_data.items():
        if (
            data.get("market_cap", 0) >= 50_000_000_000 and
            data.get("price", 0) > 100 and
            50 <= data.get("rsi", 0) <= 70 and
            data.get("macd_hist", 0) > 0 and
            data.get("volume_dod", 0) > 1.0 and
            data.get("atr", 10) <= 2.0
        ):
            result.append(symbol)
    return result

def ipo_strategy(market_data: dict) -> List[str]:
    result = []
    three_years_ago = datetime.now() - timedelta(days=3*365)
    for symbol, data in market_data.items():
        ipo_date = data.get("ipo_date")
        if isinstance(ipo_date, str):
            try:
                ipo_date = datetime.strptime(ipo_date, "%Y-%m-%d")
            except:
                continue
        if (
            ipo_date and ipo_date >= three_years_ago and
            data.get("avg_volume", 0) >= 500_000 and
            data.get("rsi", 0) >= 60 and
            data.get("macd", 0) > 0 and
            data.get("macd_hist", 0) > 0 and
            data.get("price", 0) > data.get("ema_50", 0) and
            data.get("bullish_pattern", False)
        ):
            result.append(symbol)
    return result

def get_stock_symbols_by_strategy(strategy_name: str, market_data: dict) -> List[str]:
    strategies = {
        "ultima": ultima_strategy,
        "freshman": freshman_strategy,
        "top_volume": top_volume_strategy,
        "super_leverage": super_leverage_strategy,
        "large_cap": large_cap_strategy,
        "ipo": ipo_strategy
    }
    return strategies.get(strategy_name, lambda x: [])(market_data)

def get_ranked_stock_symbols(strategies: List[str], market_data: dict, top_n: int = 5) -> List[Tuple[str, float]]:
    ranked = []
    symbols = set()
    for strategy in strategies:
        symbols.update(get_stock_symbols_by_strategy(strategy, market_data))

    for symbol in symbols:
        score = calculate_confidence(symbol, market_data.get(symbol, {}))
        ranked.append((symbol, score))

    ranked.sort(key=lambda x: x[1], reverse=True)
    return ranked[:top_n]
