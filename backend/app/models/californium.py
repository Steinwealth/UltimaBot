import joblib
import os

class CaliforniumModel:
    def __init__(self):
        model_path = os.path.join(os.path.dirname(__file__), 'joblib', 'Californium.joblib')
        self.model = joblib.load(model_path)

    def predict(self, features):
        """
        Returns prediction confidence score for trade decision.
        """
        try:
            confidence = self.model.predict_proba([features])[0][1]
            return float(confidence)
        except Exception as e:
            print(f"[CaliforniumModel] Prediction error: {e}")
            return 0.0

    def determine_power_trade_tier(self, confidence):
        """
        Assign Power Trade tier based on confidence level.
        """
        if confidence >= 0.995:
            return 3
        elif confidence >= 0.99:
            return 2
        elif confidence >= 0.95:
            return 1
        return 0
