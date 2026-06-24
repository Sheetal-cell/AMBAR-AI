import pandas as pd

from scipy.stats import (
    pearsonr
)

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

    return fire.merge(
        hcho,
        on="obs_date"
    )


def run_lag():

    df = load_data()

    results = []

    for lag in range(
        1,
        15
    ):

        shifted = (
            df["fire_count"]
            .shift(lag)
        )

        valid = (
            pd.concat(
                [
                    shifted,
                    df["mean_hcho"]
                ],
                axis=1
            )
            .dropna()
        )

        r, p = pearsonr(
            valid.iloc[:,0],
            valid.iloc[:,1]
        )

        results.append(
            {
                "lag": lag,
                "pearson": r,
                "p": p
            }
        )

    return pd.DataFrame(
        results
    )


if __name__ == "__main__":

    result = run_lag()

    print(result)