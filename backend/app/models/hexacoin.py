import joblib
import os

class HexacoinModel:
    def __init__(self):
        model_path = os.path.join(os.path.dirname(__file__), 'joblib', 'Hexacoin.joblib')
        self.model = joblib.load(model_path)

    def predict(self, features):
        """
        Returns prediction confidence based on input features.
        Applies error handling to ensure safe fallback.
        """
        try:
            confidence = self.model.predict_proba([features])[0][1]
            return float(confidence)
        except Exception as e:
            print(f"[HexacoinModel] Prediction error: {e}")
            return 0.0

    def determine_power_trade_tier(self, confidence):
        """
        Assigns Power Trade tier based on prediction confidence.
        Tier thresholds match production logic.
        """
        if confidence >= 0.995:
            return 3  # Tier 3
        elif confidence >= 0.99:
            return 2  # Tier 2
        elif confidence >= 0.95:
            return 1  # Tier 1
        return 0  # Normal trade
