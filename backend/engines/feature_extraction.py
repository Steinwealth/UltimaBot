from typing import Dict
import numpy as np


def extract_features_from_ohlcv(ohlcv: Dict) -> Dict:
    """
    Extracts normalized key features from OHLCV data for confidence + forecast engines.
    Supports multi-timeframe feature output.
    """
    close_prices = np.array(ohlcv.get("close", []))
    volume = np.array(ohlcv.get("volume", []))

    if len(close_prices) < 60:
        return {}

    returns = np.diff(np.log(close_prices))
    volatility = np.std(returns[-30:]) * np.sqrt(252)
    avg_volume = np.mean(volume[-30:])
    price_change_5min = (close_prices[-1] - close_prices[-2]) / close_prices[-2]
    price_change_30min = (close_prices[-1] - close_prices[-7]) / close_prices[-7]
    price_change_1h = (close_prices[-1] - close_prices[-13]) / close_prices[-13]
    trend_strength = np.polyfit(range(len(close_prices[-10:])), close_prices[-10:], 1)[0] / close_prices[-1]

    # Normalize features (0–1) using rolling min/max for volatility and volume
    norm_vol = (volatility - np.min(returns)) / (np.max(returns) - np.min(returns) + 1e-6)
    norm_vol = float(np.clip(norm_vol, 0, 1))
    norm_volume = float(np.clip(avg_volume / (np.max(volume) + 1e-6), 0, 1))

    return {
        "volatility": round(volatility, 6),
        "norm_volatility": round(norm_vol, 4),
        "avg_volume": round(avg_volume, 2),
        "norm_volume": round(norm_volume, 4),
        "price_change_5min": round(price_change_5min, 4),
        "price_change_30min": round(price_change_30min, 4),
        "price_change_1h": round(price_change_1h, 4),
        "trend_strength": round(trend_strength, 4)
    }
