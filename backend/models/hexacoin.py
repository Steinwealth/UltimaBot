from joblib import load

class HexacoinModel:
    def __init__(self):
        self.name = "Hexacoin"
        self.mode = "Easy"
        self.model = load("models/Hexacoin.joblib")

    def predict(self, features):
        signal = self.model.predict([features])[0]
        confidence = self.model.predict_proba([features])[0][1]
        return signal, confidence

