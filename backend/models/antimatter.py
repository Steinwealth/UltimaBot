import joblib
import os

class AntimatterModel:
    def __init__(self):
        model_path = os.path.join(os.path.dirname(__file__), '../models/antimatter.joblib')
        self.model = joblib.load(model_path)

    def predict(self, features):
        """
        Returns prediction confidence based on input features.
        Applies Power Trade scaling if needed.
        """
        try:
            confidence = self.model.predict_proba([features])[0][1]
            return confidence
        except Exception as e:
            print(f"[AntimatterModel] Prediction error: {e}")
            return 0.0  # Fallback low confidence

    def determine_power_trade_tier(self, confidence):
        """
        Determines Power Trade tier based on confidence.
        """
        if confidence >= 0.995:
            return 3  # T3
        elif confidence >= 0.99:
            return 2  # T2
        elif confidence >= 0.95:
            return 1  # T1
        return 0  # Normal trade
