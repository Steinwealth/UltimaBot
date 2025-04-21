from typing import Dict

def check_risk_constraints(
    position_size: float,
    account_balance: float,
    used_margin_pct: float,
    available_margin_pct: float,
    open_drawdown_pct: float,
    max_allowed_drawdown: float = 0.28,
    max_position_pct: float = 0.30,
    min_margin_buffer: float = 0.15
) -> Dict:
    """
    Enforce margin and risk constraints before trade approval.
    """
    exceeds_position_cap = position_size > account_balance * max_position_pct
    exceeds_drawdown_cap = open_drawdown_pct > max_allowed_drawdown
    margin_too_low = available_margin_pct < min_margin_buffer

    allowed = not (exceeds_position_cap or exceeds_drawdown_cap or margin_too_low)

    return {
        "allowed": allowed,
        "exceeds_position_cap": exceeds_position_cap,
        "exceeds_drawdown_cap": exceeds_drawdown_cap,
        "margin_too_low": margin_too_low,
        "used_margin_pct": used_margin_pct,
        "available_margin_pct": available_margin_pct,
        "open_drawdown_pct": open_drawdown_pct
    }
