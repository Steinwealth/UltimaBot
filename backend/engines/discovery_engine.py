# backend/engines/discovery_engine.py

from typing import List, Tuple
from engines.confidence_engine import calculate_confidence
from datetime import datetime, timedelta

# === STOCK STRATEGIES ===

def ultima_strategy(market_data: dict) -> List[str]:
    result = []
    for symbol, data in market_data.items():
        if (
            data.get("rsi", 0) >= 50 and data.get("macd", 0) > 0 and
            data.get("volume_surge", 0) > 1.5 and data.get("atr", 10) <= 2.8 and
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
    return [
        symbol for symbol, data in market_data.items()
        if 1 <= data.get("price", 0) <= 10 and
        data.get("relative_volume", 0) > 5 and
        data.get("volume", 0) > 100_000 and
        data.get("float", 100_000_000) < 20_000_000
    ]

def top_volume_strategy(market_data: dict) -> List[str]:
    return [
        symbol for symbol, data in market_data.items()
        if data.get("volume_rank", 999) <= 50 and
        data.get("volume", 0) >= data.get("avg_volume", 1) * 2 and
        data.get("rsi", 0) >= 50 and
        data.get("macd_recent_cross", False) and
        data.get("atr", 10) <= 3.0 and
        data.get("price", 0) >= 2
    ]

def super_leverage_strategy(market_data: dict) -> List[str]:
    leveraged_symbols = ["TQQQ", "5QQQ", "SOXL", "SPYU", "SPXL", "MSTX", "BITX", "SHNY", "UGL", "DGP"]
    return [
        symbol for symbol in leveraged_symbols
        if (symbol in market_data and
            market_data[symbol].get("volume_1min", 0) > market_data[symbol].get("avg_volume_1min", 1) * 1.3 and
            market_data[symbol].get("rsi", 0) >= 55 and
            market_data[symbol].get("macd_recent_cross", False) and
            market_data[symbol].get("atr", 0) > 2.5 and
            market_data[symbol].get("volatility_30min", 0) >= 3.0)
    ]

def large_cap_strategy(market_data: dict) -> List[str]:
    return [
        symbol for symbol, data in market_data.items()
        if data.get("market_cap", 0) >= 50_000_000_000 and
        data.get("price", 0) > 100 and
        50 <= data.get("rsi", 0) <= 70 and
        data.get("macd_hist", 0) > 0 and
        data.get("volume_dod", 0) > 1.0 and
        data.get("atr", 10) <= 2.0
    ]

def ipo_strategy(market_data: dict) -> List[str]:
    three_years_ago = datetime.now() - timedelta(days=3*365)
    return [
        symbol for symbol, data in market_data.items()
        if (isinstance(data.get("ipo_date"), datetime) and data["ipo_date"] >= three_years_ago and
            data.get("sales_growth_qoq", 0) > 30 and data.get("price_change", "") == "up" and
            data.get("avg_volume", 0) >= 500_000)
    ]

def ipo_reversal_strategy(market_data: dict) -> List[str]:
    two_years_ago = datetime.now() - timedelta(days=2*365)
    return [
        symbol for symbol, data in market_data.items()
        if (isinstance(data.get("ipo_date"), datetime) and data["ipo_date"] >= two_years_ago and
            data.get("rsi", 100) <= 40 and data.get("candlestick", "") in ["hammer", "doji"] and
            data.get("macd_cross", False) and data.get("short_interest", 0) > 10)
    ]

def low_float_momentum_strategy(market_data: dict) -> List[str]:
    return [
        symbol for symbol, data in market_data.items()
        if data.get("float", 50_000_000) < 20_000_000 and
        data.get("volume", 0) >= 1_000_000 and
        data.get("price_change_5min", 0) >= 0.05 and
        data.get("rsi", 0) >= 60 and
        data.get("breakout_above_resistance", False)
    ]

STOCK_STRATEGIES = {
    "ultima": ultima_strategy,
    "freshman": freshman_strategy,
    "top_volume": top_volume_strategy,
    "super_leverage": super_leverage_strategy,
    "large_cap": large_cap_strategy,
    "ipo": ipo_strategy,
    "ipo_reversal": ipo_reversal_strategy,
    "low_float": low_float_momentum_strategy
}

def get_stock_symbols_by_strategy(strategy_name: str, market_data: dict) -> List[str]:
    return STOCK_STRATEGIES.get(strategy_name, lambda x: [])(market_data)

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

# === CRYPTO STRATEGIES ===

def original_strategy(market_data: dict) -> List[str]:
    return [symbol for symbol, data in market_data.items() if data.get("is_major", False)]

def volume_spike_strategy(market_data: dict) -> List[str]:
    return [
        symbol for symbol, data in market_data.items()
        if data.get("volume_5min", 0) > data.get("avg_volume_5min", 1) * 2
        and data.get("rsi", 0) >= 60
        and data.get("macd_cross", False)
    ]

def micro_cap_strategy(market_data: dict) -> List[str]:
    return [
        symbol for symbol, data in market_data.items()
        if data.get("market_cap", 0) < 50_000_000
        and data.get("volume_24h", 0) > 1_000_000
        and data.get("price_change_24h", 0) >= 0.1
        and data.get("confidence", 0) >= 0.93
    ]

def mid_cap_momentum_strategy(market_data: dict) -> List[str]:
    return [
        symbol for symbol, data in market_data.items()
        if 100_000_000 <= data.get("market_cap", 0) <= 1_000_000_000
        and data.get("volume_1h", 0) > data.get("avg_volume_1h", 1) * 2
        and data.get("price_change_30min", 0) >= 0.07
        and data.get("rsi", 0) > 60
        and data.get("macd_cross", False)
    ]

def low_float_rally_strategy(market_data: dict) -> List[str]:
    return [
        symbol for symbol, data in market_data.items()
        if data.get("circulating_supply", 0) < 20_000_000
        and data.get("volume_24h", 0) >= 5_000_000
        and data.get("price_change_24h", 0) >= 0.10
        and data.get("confidence", 0) >= 0.94
        and data.get("listed_on", "").lower() in ["coinbase", "binance"]
    ]

def defi_spike_strategy(market_data: dict) -> List[str]:
    return [
        symbol for symbol, data in market_data.items()
        if data.get("sector", "").lower() == "defi"
        and data.get("volume_intraday", 0) >= data.get("avg_volume", 1) * 3
        and data.get("rsi", 0) >= 65
        and data.get("price", 0) > data.get("ema_50", 0)
    ]

def meme_momentum_strategy(market_data: dict) -> List[str]:
    return [
        symbol for symbol, data in market_data.items()
        if data.get("trending_score", 0) >= 7
        and data.get("volume_24h", 0) > 1_000_000
        and data.get("price_change_6h", 0) >= 0.08
        and data.get("confidence", 0) >= 0.91
        and any(tag in data.get("tags", []) for tag in ["meme", "momentum"])
    ]

CRYPTO_DISCOVERY_STRATEGIES = {
    "original": original_strategy,
    "volume-spike": volume_spike_strategy,
    "micro-cap": micro_cap_strategy,
    "mid-cap": mid_cap_momentum_strategy,
    "low-float": low_float_rally_strategy,
    "defi": defi_spike_strategy,
    "meme": meme_momentum_strategy
}

def get_crypto_symbols_by_strategy(strategy_name: str, market_data: dict) -> List[str]:
    return CRYPTO_DISCOVERY_STRATEGIES.get(strategy_name, lambda x: [])(market_data)

def get_ranked_crypto_symbols(strategies: List[str], market_data: dict, top_n: int = 5) -> List[Tuple[str, float]]:
    ranked = []
    symbols = set()
    for strategy in strategies:
        symbols.update(get_crypto_symbols_by_strategy(strategy, market_data))
    for symbol in symbols:
        score = calculate_confidence(symbol, market_data.get(symbol, {}))
        ranked.append((symbol, score))
    ranked.sort(key=lambda x: x[1], reverse=True)
    return ranked[:top_n]
