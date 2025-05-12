# backend/app/engines/discovery_engine/symbol_priority.py

import math
import statistics

class SymbolPriority:
    def __init__(self):
        self.memory = {}

    def update_priority(self, symbol, trade_result):
        """
        Adjusts the symbol priority based on trade result.
        :param symbol: The trading symbol (e.g., BTC-USD, AAPL)
        :param trade_result: {'gain_pct': float, 'confidence': float, 'streak': int}
        """
        if symbol not in self.memory:
            self.memory[symbol] = {
                'gain_history': [],
                'confidence_history': [],
                'streak': 0
            }

        self.memory[symbol]['gain_history'].append(trade_result['gain_pct'])
        self.memory[symbol]['confidence_history'].append(trade_result['confidence'])
        self.memory[symbol]['streak'] = trade_result['streak']

    def get_priority_symbols(self, min_trades=3):
        """
        Returns symbols ranked by weighted gain, streak, and confidence.
        """
        ranked = []

        for symbol, data in self.memory.items():
            gains = data['gain_history']
            confidences = data['confidence_history']
            streak = data['streak']

            if len(gains) < min_trades:
                continue  # Skip symbols with low sample size

            avg_gain = sum(gains) / len(gains)
            avg_confidence = sum(confidences) / len(confidences)
            gain_volatility = statistics.stdev(gains) if len(gains) > 1 else 0

            # Weight gain by confidence, penalize high volatility
            score = (avg_gain * avg_confidence) - (gain_volatility * 0.5) + (streak * 0.1)
            ranked.append((symbol, score))

        ranked.sort(key=lambda item: item[1], reverse=True)
        return [symbol for symbol, _ in ranked]

    def reset_symbol(self, symbol):
        if symbol in self.memory:
            del self.memory[symbol]

    def reset_all(self):
        self.memory.clear()
