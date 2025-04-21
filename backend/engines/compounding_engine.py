from typing import Dict

def calculate_position_size(
    balance: float,
    base_risk_pct: float,
    win_streak: int,
    max_allocation_pct: float = 0.30,
    use_loss_recovery: bool = False,
    last_trade_was_loss: bool = False
) -> float:
    """
    Determine position size using compounding logic, win streak scaling,
    and optional loss-recovery logic. Applies a max allocation cap.
    """
    base_allocation = balance * base_risk_pct
    streak_multiplier = 1.0 + (min(win_streak, 5) * 0.10)  # up to +50% after 5 wins

    if use_loss_recovery and last_trade_was_loss:
        streak_multiplier += 0.10  # extra 10% size if recovering from loss

    position = base_allocation * streak_multiplier
    max_allocation = balance * max_allocation_pct
    return round(min(position, max_allocation), 2)
