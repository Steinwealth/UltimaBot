import joblib
import os

class DianastoneModel:
    def __init__(self):
        model_path = os.path.join(os.path.dirname(__file__), 'joblib', 'Dianastone.joblib')
        self.model = joblib.load(model_path)

    def predict(self, features):
        """
        Returns prediction confidence based on input features.
        """
        try:
            confidence = self.model.predict_proba([features])[0][1]
            return float(confidence)
        except Exception as e:
            print(f"[DianastoneModel] Prediction error: {e}")
            return 0.0  # Fallback confidence

    def determine_power_trade_tier(self, confidence):
        """
        Determines Power Trade tier based on prediction confidence.
        """
        if confidence >= 0.995:
            return 3  # Tier 3
        elif confidence >= 0.99:
            return 2  # Tier 2
        elif confidence >= 0.95:
            return 1  # Tier 1
        return 0  # No boost
