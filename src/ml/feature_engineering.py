from pathlib import Path

import numpy as np
import pandas as pd

from src.utils.logging_utils import logger

INPUT_FILE = Path(
    "data/training/aqi_training.parquet"
)

OUTPUT_FILE = Path(
    "data/training/aqi_features.parquet"
)


def load_dataset():
    return pd.read_parquet(INPUT_FILE)


def create_wind_features(df):
    logger.info(
        "Creating wind features"
    )

    df["wind_speed"] = np.sqrt(
        df["u10"] ** 2 +
        df["v10"] ** 2
    )

    df["wind_direction"] = np.degrees(
        np.arctan2(
            df["v10"],
            df["u10"]
        )
    )

    return df


def create_pollution_ratios(df):
    logger.info(
        "Creating pollution ratios"
    )

    eps = 1e-6

    df["no2_so2_ratio"] = (
        df["no2_col"] /
        (df["so2_col"] + eps)
    )

    df["co_no2_ratio"] = (
        df["co_col"] /
        (df["no2_col"] + eps)
    )

    df["o3_hcho_ratio"] = (
        df["o3_col"] /
        (df["hcho_col"] + eps)
    )

    return df


def create_interactions(df):
    logger.info(
        "Creating interaction features"
    )

    df["aod_temp"] = (
        df["aod_550"] *
        df["t2m"]
    )

    df["fire_hcho"] = (
        df["fire_count"] *
        df["hcho_col"]
    )

    df["fire_aod"] = (
        df["fire_count"] *
        df["aod_550"]
    )

    return df


def create_log_features(df):
    logger.info(
        "Creating log features"
    )

    columns = [
        "aod_550",
        "co_col",
        "hcho_col",
        "fire_count"
    ]

    for col in columns:
        df[f"log_{col}"] = np.log1p(
            df[col]
        )

    return df


def remove_outliers(df):
    logger.info(
        "Removing extreme outliers"
    )

    numeric_cols = df.select_dtypes(
        include=np.number
    ).columns

    for col in numeric_cols:
        q1 = df[col].quantile(0.01)
        q99 = df[col].quantile(0.99)

        df[col] = df[col].clip(
            lower=q1,
            upper=q99
        )

    return df


def save_dataset(df):
    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    df.to_parquet(
        OUTPUT_FILE,
        index=False
    )

    logger.info(
        f"Saved features -> {OUTPUT_FILE}"
    )


def main():
    logger.info(
        "Loading training dataset"
    )

    df = load_dataset()

    df = create_wind_features(df)

    df = create_pollution_ratios(df)

    df = create_interactions(df)

    df = create_log_features(df)

    df = remove_outliers(df)

    save_dataset(df)


if __name__ == "__main__":
    main()