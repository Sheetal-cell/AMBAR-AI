from pathlib import Path

import geopandas as gpd
import pandas as pd
from sqlalchemy import create_engine

from src.config.settings import settings
from src.utils.logging_utils import logger

OUTPUT_DIR = Path("data/training")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

engine = create_engine(settings.DATABASE_URL)


def load_satellite():
    query = """
    SELECT
        id,
        obs_date,
        geom,
        no2_col,
        so2_col,
        co_col,
        o3_col,
        hcho_col,
        aod_550,
        qa_value
    FROM satellite_obs
    WHERE qa_value >= 0.75
    """

    return gpd.read_postgis(
        query,
        engine,
        geom_col="geom"
    )


def load_weather():
    query = """
    SELECT
        id,
        obs_date,
        geom,
        u10,
        v10,
        t2m,
        sp,
        blh,
        tp
    FROM era5_meteo
    """

    return gpd.read_postgis(
        query,
        engine,
        geom_col="geom"
    )


def load_cpcb():
    query = """
    SELECT
        station_id,
        obs_datetime,
        geom,
        aqi,
        pm25,
        pm10
    FROM cpcb_aqi
    WHERE aqi IS NOT NULL
    """

    return gpd.read_postgis(
        query,
        engine,
        geom_col="geom"
    )


def load_fire():
    query = """
    SELECT
        obs_date,
        geom,
        fire_count,
        avg_frp
    FROM fire_grid_daily
    """

    return gpd.read_postgis(
        query,
        engine,
        geom_col="geom"
    )


def join_satellite_weather(
    satellite,
    weather
):
    logger.info("Joining satellite and weather")

    merged = gpd.sjoin_nearest(
        satellite,
        weather,
        how="left",
        distance_col="distance_weather"
    )

    return merged


def join_cpcb(
    merged,
    cpcb
):
    logger.info("Joining CPCB labels")

    cpcb["obs_date"] = pd.to_datetime(
        cpcb["obs_datetime"]
    ).dt.date

    merged["obs_date"] = pd.to_datetime(
        merged["obs_date"]
    ).dt.date

    merged = merged.rename(
        columns={"obs_date": "date"}
    )

    cpcb = cpcb.rename(
        columns={"obs_date": "date"}
    )

    spatial = gpd.sjoin_nearest(
        cpcb,
        merged,
        how="inner",
        distance_col="distance_station"
    )

    return spatial


def join_fire(
    dataset,
    fire
):
    logger.info("Joining fire features")

    fire["obs_date"] = pd.to_datetime(
        fire["obs_date"]
    ).dt.date

    dataset["date"] = pd.to_datetime(
        dataset["date"]
    ).dt.date

    fire = fire.rename(
        columns={"obs_date": "date"}
    )

    merged = gpd.sjoin_nearest(
        dataset,
        fire,
        how="left",
        distance_col="distance_fire"
    )

    return merged


def clean_dataset(df):
    keep = [
        "aqi",
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
        "tp",
        "fire_count",
        "avg_frp"
    ]

    df = df[keep]

    df = df.dropna()

    return df


def main():
    logger.info("Loading datasets")

    satellite = load_satellite()
    weather = load_weather()
    cpcb = load_cpcb()
    fire = load_fire()

    merged = join_satellite_weather(
        satellite,
        weather
    )

    merged = join_cpcb(
        merged,
        cpcb
    )

    merged = join_fire(
        merged,
        fire
    )

    dataset = clean_dataset(
        merged
    )

    output_file = (
        OUTPUT_DIR /
        "aqi_training.parquet"
    )

    dataset.to_parquet(
        output_file,
        index=False
    )

    logger.info(
        f"Saved training data -> {output_file}"
    )


if __name__ == "__main__":
    main()