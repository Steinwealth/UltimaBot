from joblib import load

class AlphacoinModel:
    def __init__(self):
        self.name = "Alphacoin v4"
        self.mode = "Hard"
        self.model = load("models/Alphacoin.joblib")

    def predict(self, features):
        signal = self.model.predict([features])[0]
        confidence = self.model.predict_proba([features])[0][1]
        return signal, confidence
