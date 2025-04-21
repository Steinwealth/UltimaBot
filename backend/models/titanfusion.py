from joblib import load

class TitanFusionModel:
    def __init__(self):
        self.name = "TitanFusion"
        self.mode = "Hard"
        self.model = load("models/TitanFusion.joblib")

    def predict(self, features):
        signal = self.model.predict([features])[0]
        confidence = self.model.predict_proba([features])[0][1]
        return signal, confidence
