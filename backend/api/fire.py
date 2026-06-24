from fastapi import APIRouter
from sqlalchemy import create_engine
import pandas as pd

from src.config.settings import settings

router = APIRouter()

engine = create_engine(
    settings.DATABASE_URL
)


@router.get("/correlation")
def correlation():

    query = """
    SELECT *
    FROM fire_hcho_correlation
    ORDER BY analysis_date DESC
    """

    df = pd.read_sql(
        query,
        engine
    )

    return df.to_dict(
        orient="records"
    )


@router.get("/lag")
def lag_analysis():

    df = pd.read_csv(
        "data/results/lag_analysis.csv"
    )

    return df.to_dict(
        orient="records"
    )