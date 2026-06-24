import pandas as pd
import geopandas as gpd

from sqlalchemy import create_engine
from src.config.settings import settings

engine = create_engine(
    settings.DATABASE_URL
)


def load_hotspots():

    query = """
    SELECT
        cluster_id,
        detection_date,
        centroid
    FROM hcho_hotspots
    """

    return gpd.read_postgis(
        query,
        engine,
        geom_col="centroid"
    )


def calculate_persistence(df):

    persistence = (
        df.groupby("cluster_id")
        ["detection_date"]
        .nunique()
        .reset_index()
    )

    persistence.columns = [
        "cluster_id",
        "persistence_days"
    ]

    return persistence


def update_database(persistence):

    with engine.begin() as conn:

        for _, row in persistence.iterrows():

            conn.execute(
                """
                UPDATE hcho_hotspots
                SET persistence_days=:days
                WHERE cluster_id=:cluster
                """,
                {
                    "days":
                        int(
                            row[
                                "persistence_days"
                            ]
                        ),
                    "cluster":
                        int(
                            row[
                                "cluster_id"
                            ]
                        )
                }
            )


def main():

    hotspots = load_hotspots()

    persistence = (
        calculate_persistence(
            hotspots
        )
    )

    update_database(
        persistence
    )


if __name__ == "__main__":
    main()