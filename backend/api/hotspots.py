from fastapi import APIRouter
from sqlalchemy import create_engine
import geopandas as gpd

from src.config.settings import settings

router = APIRouter()

engine = create_engine(
    settings.DATABASE_URL
)


@router.get("/")
def hotspots():

    query = """
    SELECT *
    FROM hcho_hotspots
    """

    gdf = gpd.read_postgis(
        query,
        engine,
        geom_col="geom"
    )

    return gdf.to_json()


@router.get("/top")
def top_hotspots():

    query = """
    SELECT
        cluster_id,
        mean_hcho,
        max_hcho,
        persistence_days
    FROM hcho_hotspots
    ORDER BY max_hcho DESC
    LIMIT 20
    """

    gdf = gpd.read_postgis(
        query,
        engine
    )

    return gdf.to_dict(
        orient="records"
    )