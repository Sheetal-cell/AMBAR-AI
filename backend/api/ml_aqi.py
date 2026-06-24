from fastapi import APIRouter
from pydantic import BaseModel

from src.ml.predict_aqi import predictor

router = APIRouter()


class AQIInput(BaseModel):
    pm25: float
    pm10: float
    no2: float
    so2: float
    co: float
    o3: float
    temperature: float
    humidity: float
    wind_speed: float


@router.post("/predict")
def predict_aqi(data: AQIInput):

    pred = predictor.predict(
        data.model_dump()
    )

    return {
        "predicted_aqi": pred
    }