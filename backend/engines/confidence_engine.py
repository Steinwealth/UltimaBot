from typing import Dict
import random

def calculate_confidence(symbol: str, data: Dict) -> float:
    """
    Estimate model confidence using trend, volume, sentiment, and correlation features.
    """
    base = 0.90
    trend = data.get("trend_strength", 1.0)
    volume_factor = min(data.get("volume", 1000000) / 1_000_000, 2.0)
    correlation = data.get("correlation_score", 0.95)
    sentiment = data.get("sentiment_score", 0.9)

    # Random influence for simulation purposes
    volatility_penalty = random.uniform(0.0, 0.02)
    confidence = base + (trend * 0.02) + ((volume_factor - 1) * 0.01) + ((correlation - 0.9) * 0.5) + ((sentiment - 0.9) * 0.3)
    confidence = round(min(max(confidence - volatility_penalty, 0.85), 0.999), 3)
    return confidence
