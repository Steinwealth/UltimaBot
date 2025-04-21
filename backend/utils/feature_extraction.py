from typing import Dict
import numpy as np


def extract_features_from_ohlcv(ohlcv: Dict) -> Dict:
    """
    Extracts key features from OHLCV data for confidence + forecast engines.
    """
    close_prices = np.array(ohlcv.get("close", []))
    volume = np.array(ohlcv.get("volume", []))

    if len(close_prices) < 2:
        return {}

    returns = np.diff(np.log(close_prices))
    volatility = np.std(returns[-30:]) * np.sqrt(252)
    avg_volume = np.mean(volume[-30:])
    price_change_5min = (close_prices[-1] - close_prices[-2]) / close_prices[-2]
    trend_strength = np.polyfit(range(len(close_prices[-10:])), close_prices[-10:], 1)[0] / close_prices[-1]

    return {
        "volatility": round(volatility, 6),
        "avg_volume": round(avg_volume, 2),
        "price_change_5min": round(price_change_5min, 4),
        "trend_strength": round(trend_strength, 4)
    }
