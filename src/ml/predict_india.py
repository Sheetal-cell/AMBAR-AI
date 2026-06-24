from pathlib import Path

import joblib
import pandas as pd

from sqlalchemy import create_engine
from src.config.settings import settings
from src.utils.logging_utils import logger

engine = create_engine(
    settings.DATABASE_URL
)

MODEL_PATH = Path(
    "models/xgboost/aqi_xgb_v1.pkl"
)


def load_model():
    return joblib.load(
        MODEL_PATH
    )


def load_prediction_features():

    query = """
    SELECT
        s.obs_date,
        ST_X(s.geom) AS lon,
        ST_Y(s.geom) AS lat,
        s.geom,
        s.aod_550,
        s.no2_col,
        s.so2_col,
        s.co_col,
        s.o3_col,
        s.hcho_col,
        e.u10,
        e.v10,
        e.t2m,
        e.sp,
        e.blh,
        e.tp
    FROM satellite_obs s
    JOIN era5_meteo e
    ON s.obs_date=e.obs_date
    """

    return pd.read_sql(
        query,
        engine
    )


def category(aqi):

    if aqi <= 50:
        return "Good"

    if aqi <= 100:
        return "Satisfactory"

    if aqi <= 200:
        return "Moderate"

    if aqi <= 300:
        return "Poor"

    if aqi <= 400:
        return "Very Poor"

    return "Severe"


def main():

    model = load_model()

    df = load_prediction_features()

    feature_cols = [
        "aod_550",
        "no2_col",
        "so2_col",
        "co_col",
        "o3_col",
        "hcho_col",
        "u10",
        "v10",
        "t2m",
        "sp",
        "blh",
        "tp"
    ]

    preds = model.predict(
        df[feature_cols]
    )

    df["aqi_pred"] = preds

    df["aqi_category"] = (
        df["aqi_pred"]
        .apply(category)
    )

    results = df[
        [
            "obs_date",
            "geom",
            "aqi_pred",
            "aqi_category"
        ]
    ]

    results.to_sql(
        "aqi_predictions",
        engine,
        if_exists="append",
        index=False
    )

    logger.info(
        "AQI predictions saved"
    )


if __name__ == "__main__":
    main()