from fastapi import APIRouter
from sqlalchemy import create_engine
import pandas as pd

from src.config.settings import settings

router = APIRouter()

engine = create_engine(settings.DATABASE_URL)


@router.get("/predictions")
def get_predictions():

    query = """
    SELECT
        pred_date,
        lon,
        lat,
        aqi_pred,
        aqi_category
    FROM aqi_predictions
    LIMIT 10000
    """

    df = pd.read_sql(
        query,
        engine
    )

    return df.to_dict(
        orient="records"
    )


@router.get("/summary")
def summary():

    query = """
    SELECT
        AVG(aqi_pred) AS avg_aqi,
        MAX(aqi_pred) AS max_aqi,
        MIN(aqi_pred) AS min_aqi
    FROM aqi_predictions
    """

    result = pd.read_sql(
        query,
        engine
    )

    return result.iloc[0].to_dict()