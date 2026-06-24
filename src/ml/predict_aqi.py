import joblib
import pandas as pd

MODEL_PATH = "models/xgboost/aqi_model.pkl"


class AQIPredictor:

    def __init__(self):
        self.model = joblib.load(MODEL_PATH)

    def predict(self, data: dict):

        df = pd.DataFrame([data])

        prediction = self.model.predict(df)[0]

        return round(float(prediction), 2)


predictor = AQIPredictor()