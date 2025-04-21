from typing import Dict

def calculate_position_size(balance: float, base_risk_pct: float, win_streak: int, max_allocation_pct: float = 0.30) -> float:
    """
    Determine position size using compounding logic, win streak scaling, and risk cap.
    """
    base_allocation = balance * base_risk_pct
    streak_multiplier = 1.0 + (min(win_streak, 5) * 0.10)  # +10% per win, max +50%
    position = base_allocation * streak_multiplier
    max_allocation = balance * max_allocation_pct
    return round(min(position, max_allocation), 2)
