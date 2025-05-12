# backend/engines/strategy_engine/mode_manager.py

class ModeManager:
    MODES = {
        'Easy': {
            'confidence_floor': 0.93,
            'max_scaling': 2.0,
            'risk_tolerance': 'low',
            'trailing_sl_buffer': 0.01,  # Wider stop-loss buffer
        },
        'Hard': {
            'confidence_floor': 0.95,
            'max_scaling': 3.0,
            'risk_tolerance': 'medium',
            'trailing_sl_buffer': 0.005,
        },
        'Hero': {
            'confidence_floor': 0.98,
            'max_scaling': 5.0,
            'risk_tolerance': 'high',
            'trailing_sl_buffer': 0.002,
        }
    }

    def __init__(self, mode='Easy'):
        if mode not in self.MODES:
            raise ValueError(f"Invalid mode: {mode}")
        self.mode = mode
        self.settings = self.MODES[mode]

    def get_confidence_floor(self):
        return self.settings['confidence_floor']

    def get_max_scaling(self):
        return self.settings['max_scaling']

    def get_risk_tolerance(self):
        return self.settings['risk_tolerance']

    def get_trailing_sl_buffer(self):
        return self.settings['trailing_sl_buffer']

    def set_mode(self, mode):
        if mode not in self.MODES:
            raise ValueError(f"Invalid mode: {mode}")
        self.mode = mode
        self.settings = self.MODES[mode]
        print(f"[ModeManager] Switched to {mode} mode.")
