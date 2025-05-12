# backend/app/engines/risk_engine/risk_manager.py

class RiskManager:
    def __init__(self, mode_settings=None):
        mode_settings = mode_settings or {}
        self.margin_floor_buffer = mode_settings.get("margin_floor_buffer", 0.20)  # 20% Margin Floor Buffer
        self.max_account_risk = mode_settings.get("max_account_risk", 0.25)
        self.max_trade_risk = mode_settings.get("max_trade_risk", 0.02)  # 2% Per-Trade Risk
        self.allocation_percent = mode_settings.get("allocation_percent", 0.75)
        self.confidence_buffer = 0.20  # 20% Confidence Buffer

    # Capital allocation (75% cash + margin)
    def calculate_available_capital(self, account_data):
        cash_available = account_data.get('cash_available', 0.0)
        buying_power = account_data.get('buying_power', cash_available)
        margin_balance = account_data.get('margin_balance', 0.0)
        margin_enabled = account_data.get('margin_enabled', False)
        total_funds = buying_power + (margin_balance if margin_enabled else 0)
        return total_funds * self.allocation_percent

    # Margin floor (20%)
    def check_margin_floor(self, account_data):
        buying_power = account_data.get('buying_power', 0.0)
        margin_balance = account_data.get('margin_balance', 0.0)
        margin_used = account_data.get('margin_used', 0.0)
        margin_enabled = account_data.get('margin_enabled', False)
        total_funds = buying_power + (margin_balance if margin_enabled else 0)
        funds_remaining = total_funds - margin_used
        return (funds_remaining / total_funds) >= self.margin_floor_buffer if total_funds > 0 else False

    # Drawdown protection
    def check_account_risk(self, account_balance, account_drawdown):
        drawdown_percent = account_drawdown / account_balance
        return drawdown_percent <= self.max_account_risk

    # Per-trade risk (2%)
    def check_trade_risk(self, trade_risk_amount, account_balance):
        trade_risk_percent = trade_risk_amount / account_balance
        return trade_risk_percent <= self.max_trade_risk

    # Power Trade tiering (T1–T3) with confidence buffer
    def get_power_trade_tier(self, confidence, recent_confidence=None):
        if recent_confidence is not None and (recent_confidence - confidence) > self.confidence_buffer:
            return 0  # Skip scaling if confidence dipped recently

        if confidence >= 0.995:
            return 3
        elif confidence >= 0.985:
            return 2
        elif confidence >= 0.96:
            return 1
        return 0

    # Scaling multiplier with win streak boost
    def get_scaling_multiplier(self, power_tier, win_streak=0):
        multipliers = {0: 1.0, 1: 1.5, 2: 2.0, 3: 3.0}
        multiplier = multipliers.get(power_tier, 1.0)

        if win_streak >= 3:
            multiplier *= 1.25  # Boost scaling by 25% after 3+ wins
        return multiplier

    # Volatility filter (ATR% ≤ 5%)
    def check_volatility_filter(self, atr, price):
        atr_percent = atr / price if price > 0 else 0
        return atr_percent <= 0.05
