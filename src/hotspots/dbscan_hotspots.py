from sklearn.cluster import DBSCAN
import pandas as pd
import geopandas as gpd

from sqlalchemy import create_engine

from src.config.settings import settings

engine = create_engine(
    settings.DATABASE_URL
)


def load_hcho():

    query = """
    SELECT
        obs_date,
        geom,
        hcho_col
    FROM satellite_obs
    WHERE hcho_col IS NOT NULL
    """

    return gpd.read_postgis(
        query,
        engine,
        geom_col="geom"
    )


def detect_hotspots(
    gdf,
    eps=0.3,
    min_samples=10
):

    coords = list(
        zip(
            gdf.geometry.y,
            gdf.geometry.x
        )
    )

    model = DBSCAN(
        eps=eps,
        min_samples=min_samples
    )

    gdf["cluster"] = (
        model.fit_predict(
            coords
        )
    )

    return gdf


def main():

    gdf = load_hcho()

    hotspots = detect_hotspots(
        gdf
    )

    hotspots.to_file(
        "data/exports/hcho_hotspots.geojson",
        driver="GeoJSON"
    )


if __name__ == "__main__":
    main()