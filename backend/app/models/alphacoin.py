import joblib
import os

class AlphacoinModel:
    def __init__(self):
        model_path = os.path.join(os.path.dirname(__file__), 'joblib', 'Alphacoin.joblib')
        self.model = joblib.load(model_path)

    def predict(self, features):
        """
        Returns prediction confidence based on input features.
        """
        try:
            confidence = self.model.predict_proba([features])[0][1]
            return confidence
        except Exception as e:
            print(f"[AlphacoinModel] Prediction error: {e}")
            return 0.0

    def determine_power_trade_tier(self, confidence):
        """
        Determines Power Trade tier based on confidence score.
        """
        if confidence >= 0.995:
            return 3
        elif confidence >= 0.99:
            return 2
        elif confidence >= 0.95:
            return 1
        return 0
