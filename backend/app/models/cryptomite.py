import joblib
import os

class CryptomiteModel:
    def __init__(self):
        model_path = os.path.join(os.path.dirname(__file__), 'joblib', 'Cryptomite.joblib')
        self.model = joblib.load(model_path)

    def predict(self, features):
        """
        Predicts confidence score based on features.
        """
        try:
            confidence = self.model.predict_proba([features])[0][1]
            return float(confidence)
        except Exception as e:
            print(f"[CryptomiteModel] Prediction error: {e}")
            return 0.0

    def determine_power_trade_tier(self, confidence):
        """
        Maps confidence to Power Trade tier.
        """
        if confidence >= 0.995:
            return 3
        elif confidence >= 0.99:
            return 2
        elif confidence >= 0.95:
            return 1
        return 0
