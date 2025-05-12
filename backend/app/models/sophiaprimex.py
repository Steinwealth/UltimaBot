import joblib
import os

class SophiaPrimeXModel:
    def __init__(self):
        model_path = os.path.join(os.path.dirname(__file__), 'joblib', 'SophiaPrimeX.joblib')
        self.model = joblib.load(model_path)

    def predict(self, features):
        """
        Returns prediction confidence from SophiaPrimeX.
        """
        try:
            confidence = self.model.predict_proba([features])[0][1]
            return float(confidence)
        except Exception as e:
            print(f"[SophiaPrimeXModel] Prediction error: {e}")
            return 0.0

    def determine_power_trade_tier(self, confidence):
        """
        Power Trade tier assignment based on confidence.
        """
        if confidence >= 0.995:
            return 3
        elif confidence >= 0.99:
            return 2
        elif confidence >= 0.95:
            return 1
        return 0
