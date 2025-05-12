# backend/engines/strategy_engine/strategy_manager.py

class StrategyManager:
    VALID_STRATEGIES = [
        'CoinMarketCap', 'Micro Cap Moonshot', '100X Volume Spike', 'Pump.Fun Trending', 'GMGN Trending',
        'original', 'mid_low_cap',
        'freshman', 'top_volume', 'large_cap', 'super_leverage', 'cameron'
    ]

    def __init__(self, symbol_priority, confidence_floor=0.96):
        self.symbol_priority = symbol_priority
        self.confidence_floor = confidence_floor
        self.strategies = self.VALID_STRATEGIES.copy()

    def get_active_strategies(self, confidence_tracker):
        """
        Return strategies with average confidence above threshold.
        """
        active_strategies = []
        for strategy in self.strategies:
            try:
                avg_conf = confidence_tracker.get_avg_confidence(strategy)
                if avg_conf >= self.confidence_floor:
                    active_strategies.append(strategy)
            except Exception as e:
                continue  # Handle missing confidence data gracefully
        return active_strategies

    def get_scaling_multiplier(self, confidence, mode="easy"):
        """
        Adjust position size scaling based on confidence bands and mode.
        """
        if mode == "hard":
            if confidence > 0.998:
                return 5.0
            elif confidence > 0.995:
                return 4.0
            elif confidence > 0.99:
                return 3.0
            else:
                return 1.0
        else:  # Easy Mode
            if confidence > 0.995:
                return 3.5
            elif confidence > 0.99:
                return 2.5
            elif confidence > 0.975:
                return 2.0
            else:
                return 1.0

    def prioritize_strategies(self):
        """
        Dynamically reorder strategies based on SymbolPriority rankings.
        """
        top_symbols = self.symbol_priority.get_priority_symbols()
        priority_boost = {s: 0 for s in self.strategies}

        symbol_strategy_map = {
            'WIF': ['Micro Cap Moonshot', '100X Volume Spike'],
            'BTC-USD': ['original', 'large_cap'],
            'ETH-USD': ['original', 'large_cap'],
            'FLOKI': ['Micro Cap Moonshot', 'mid_low_cap'],
            'SOL-USD': ['original', 'large_cap'],
        }

        for symbol in top_symbols[:5]:
            for strategy in symbol_strategy_map.get(symbol, []):
                if strategy in priority_boost:
                    priority_boost[strategy] += 1

        # Boost Power Trades and Moonshots globally
        for strategy in priority_boost:
            if strategy in ['Micro Cap Moonshot', '100X Volume Spike']:
                priority_boost[strategy] += 2

        self.strategies.sort(key=lambda s: priority_boost[s], reverse=True)
