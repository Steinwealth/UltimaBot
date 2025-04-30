class CompoundingEngine:
    def __init__(self, base_allocation_pct=10, max_compound_factor=3.0, mode='easy'):
        """
        :param base_allocation_pct: Starting % of available capital per trade.
        :param max_compound_factor: Max multiplier cap.
        :param mode: Trading mode ('easy' or 'hard').
        """
        self.base_allocation_pct = base_allocation_pct
        self.max_compound_factor = max_compound_factor
        self.current_factor = 1.0
        self.mode = mode

    def adjust_for_streak(self, win_streak, drawdown=0.0, confidence=0.95):
        """
        Adjusts compounding multiplier based on win streak, drawdown, and confidence.
        """
        if drawdown > 0.1:  # If drawdown exceeds 10%, reset
            self.current_factor = 1.0
            return

        if win_streak <= 0:
            self.current_factor = 1.0
        else:
            # Base scaling on mode and win streak
            if self.mode == 'easy':
                streak_factor = 1.0 + (win_streak * 0.1)
                confidence_boost = 1.0 + max(0, (confidence - 0.96) * 5)  # Confidence boost starts at 0.96+
                self.current_factor = min(streak_factor * confidence_boost, 2.5)
            elif self.mode == 'hard':
                streak_factor = 1.0 + (win_streak * 0.3)
                confidence_boost = 1.0 + max(0, (confidence - 0.96) * 6)  # Hard mode more aggressive
                self.current_factor = min(streak_factor * confidence_boost, 5.0)

    def calculate_position_size(self, available_capital):
        """
        Calculates position size dynamically based on available capital.
        """
        base_position = available_capital * (self.base_allocation_pct / 100)
        return round(base_position * self.current_factor, 2)  # Round for broker constraints

    def reset(self):
        """
        Resets compounding multiplier.
        """
        self.current_factor = 1.0
