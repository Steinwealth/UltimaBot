from joblib import load

class DianastoneModel:
    def __init__(self):
        self.name = "Dianastone"
        self.mode = "Easy"
        self.model = load("models/Dianastone.joblib")

    def predict(self, features):
        signal = self.model.predict([features])[0]
        confidence = self.model.predict_proba([features])[0][1]
        return signal, confidence

