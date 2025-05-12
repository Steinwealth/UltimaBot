# backend/engines/strategy_engine/reentry_manager.py

class ReentryManager:
    def __init__(self):
        self.reentry_memory = {}

    def record_exit(self, symbol, exit_reason, confidence, gain_pct):
        """
        Store exit data for potential reentry decisions.
        """
        self.reentry_memory[symbol] = {
            'exit_reason': exit_reason,
            'confidence': confidence,
            'gain_pct': gain_pct
        }

    def should_reenter(self, symbol, current_confidence, current_gain_pct):
        """
        Determine if reentry should be triggered based on symbol memory.
        """
        if symbol not in self.reentry_memory:
            return False

        last_exit = self.reentry_memory[symbol]

        # Reenter if confidence remains high and potential gain exceeds last exit
        if (current_confidence > last_exit['confidence'] * 0.95 and
                current_gain_pct > last_exit['gain_pct'] * 1.1):
            return True

        return False

    def clear_symbol(self, symbol):
        if symbol in self.reentry_memory:
            del self.reentry_memory[symbol]

    def clear_all(self):
        self.reentry_memory.clear()
