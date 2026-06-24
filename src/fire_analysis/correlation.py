from scipy.stats import (
    pearsonr,
    spearmanr
)

import pandas as pd

from sqlalchemy import (
    create_engine
)

from src.config.settings import settings

engine = create_engine(
    settings.DATABASE_URL
)


def load_data():

    fire = pd.read_sql(
        """
        SELECT
            obs_date,
            fire_count
        FROM fire_grid_daily
        """,
        engine
    )

    hcho = pd.read_sql(
        """
        SELECT
            obs_date,
            AVG(hcho_col)
            AS mean_hcho
        FROM satellite_obs
        GROUP BY obs_date
        """,
        engine
    )

    return fire, hcho


def compute():

    fire, hcho = load_data()

    merged = fire.merge(
        hcho,
        on="obs_date"
    )

    pearson = pearsonr(
        merged["fire_count"],
        merged["mean_hcho"]
    )

    spearman = spearmanr(
        merged["fire_count"],
        merged["mean_hcho"]
    )

    print(
        "Pearson:",
        pearson
    )

    print(
        "Spearman:",
        spearman
    )


if __name__ == "__main__":
    compute()