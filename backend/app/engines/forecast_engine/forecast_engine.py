# backend/engines/forecast_engine/forecast_engine.py

import numpy as np

class ForecastEngine:
    def __init__(self, mode_settings):
        # Mode-sensitive TP/SL scaling
        self.mode = mode_settings.get("mode", "easy")
        self.trail_to_moon_active = mode_settings.get("trail_to_moon_active", True)

        # Expanded multipliers for TP and SL curves
        self.tp_multipliers = {
            "easy": 2.0,
            "hard": 3.0
        }
        self.sl_multipliers = {
            "easy": 0.9,
            "hard": 0.7
        }

        # Trailing stop anchors
        self.trailing_anchors = {
            "easy": 0.75,  # Trails at 75% of peak move
            "hard": 0.55   # Trails at 55% of peak move (Deep Hold)
        }

    def forecast(self, highs, lows, closes, breakout_velocity=0):
        """
        Generate TP and SL forecasts based on ATR, trend strength, mode, and Trail-to-Moon logic.
        """
        atr = self.calculate_atr(highs, lows, closes)
        trend_strength = self.calculate_trend_strength(closes)

        tp_multiplier = self.tp_multipliers[self.mode]
        sl_multiplier = self.sl_multipliers[self.mode]

        base_tp = atr * tp_multiplier * trend_strength
        sl = atr * sl_multiplier / trend_strength

        # Apply Trail-to-Moon extension if active
        if self.trail_to_moon_active and breakout_velocity > 0:
            extended_tp = base_tp * (1 + breakout_velocity)
        else:
            extended_tp = base_tp

        confidence = self.calculate_confidence(trend_strength)

        return {
            "tp": extended_tp,
            "sl": sl,
            "confidence": confidence,
            "trailing_anchor": self.trailing_anchors[self.mode]
        }

    def calculate_atr(self, highs, lows, closes, period=14):
        trs = []
        for i in range(1, len(closes)):
            tr = max(highs[i] - lows[i], abs(highs[i] - closes[i-1]), abs(lows[i] - closes[i-1]))
            trs.append(tr)
        return np.mean(trs[-period:])

    def calculate_trend_strength(self, closes):
        recent = closes[-5:]
        slope = (recent[-1] - recent[0]) / 5
        volatility = np.std(recent)
        if volatility == 0:
            return 1.0
        return max(1.0, abs(slope) / volatility)

    def calculate_confidence(self, trend_strength):
        return min(1.0, 0.9 + (trend_strength - 1.0) * 0.05)
