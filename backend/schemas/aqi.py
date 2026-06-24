from pydantic import BaseModel


class AQIPrediction(BaseModel):

    lat: float
    lon: float

    aqi_pred: float

    aqi_category: str