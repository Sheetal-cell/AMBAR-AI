from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):

    COPERNICUS_USER: str
    COPERNICUS_PASS: str

    CDSE_CLIENT_ID: str
    CDSE_CLIENT_SECRET: str

    CDS_URL: str
    CDS_KEY: str

    FIRMS_MAP_KEY: str

    MOSDAC_USER: str
    MOSDAC_PASS: str

    CPCB_API_KEY: str

    DATABASE_URL: str

    REDIS_URL: str

    SECRET_KEY: str

    NEXT_PUBLIC_API_URL: str

    NEXT_PUBLIC_MAPBOX_TOKEN: str

    class Config:
        env_file = ".env"


@lru_cache
def get_settings():
    return Settings()


settings = get_settings()