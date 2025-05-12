# backend/app/engines/risk_engine/power_trade_scaling.py

class PowerTradeScaler:
    def __init__(self, max_tier=3):
        """
        :param max_tier: Limits the maximum Power Trade tier (default T3).
        """
        self.max_tier = max_tier
        self.tiers = {
            0: {"confidence": 0.0,    "multiplier": 1.0},   # Normal
            1: {"confidence": 0.95,  "multiplier": 1.5},   # T1
            2: {"confidence": 0.99,  "multiplier": 2.0},   # T2
            3: {"confidence": 0.995, "multiplier": 3.0}    # T3
        }

    def determine_tier(self, confidence):
        """
        Determine Power Trade tier based on confidence.
        """
        for tier in reversed(range(self.max_tier + 1)):
            if confidence >= self.tiers[tier]["confidence"]:
                return tier
        return 0

    def get_multiplier(self, tier):
        """
        Returns the multiplier for the given Power Trade tier.
        """
        return self.tiers.get(tier, {"multiplier": 1.0})["multiplier"]

    def apply_scaling(self, base_position_size, confidence):
        """
        Applies Power Trade scaling to the base position size based on confidence.
        """
        tier = self.determine_tier(confidence)
        multiplier = self.get_multiplier(tier)
        scaled_position = base_position_size * multiplier
        return scaled_position, tier
