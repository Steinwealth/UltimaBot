# forecast_engine/reaction_curve.py

import numpy as np

class ReactionCurve:
    def __init__(self):
        self.curve_sensitivity = 0.05  # Base sensitivity for confidence adjustments

    def adjust_confidence(self, confidence, price_move_percent, volatility, trend_strength):
        """
        Adjust the forecast confidence score based on market reactions like price move %, volatility, and trend.
        :param confidence: Initial forecast confidence (0.90 - 1.0).
        :param price_move_percent: % price movement from entry.
        :param volatility: Current volatility measure.
        :param trend_strength: Current trend strength.
        :return: Adjusted confidence score.
        """
        reaction_factor = self.calculate_reaction_factor(price_move_percent, volatility, trend_strength)
        adjusted_confidence = confidence * (1 + reaction_factor)

        # Clamp between 0.85 and 1.0
        return max(0.85, min(adjusted_confidence, 1.0))

    def calculate_reaction_factor(self, price_move_percent, volatility, trend_strength):
        """
        Derive a reaction factor based on market dynamics.
        """
        # Positive reaction for strong trends and low volatility
        if trend_strength > 1.2 and volatility < 2.0:
            return self.curve_sensitivity * (price_move_percent / 100)

        # Negative reaction for high volatility
        if volatility > 3.0:
            return -self.curve_sensitivity * (volatility / 3)

        # Neutral market
        return 0.0
