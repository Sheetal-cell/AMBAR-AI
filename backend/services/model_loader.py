from pathlib import Path
import joblib

MODEL_PATH = Path(
    "models/xgboost/aqi_xgb_v1.pkl"
)

model = joblib.load(
    MODEL_PATH
)