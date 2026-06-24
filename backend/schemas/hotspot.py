from pydantic import BaseModel


class Hotspot(BaseModel):

    cluster_id: int

    mean_hcho: float

    max_hcho: float

    persistence_days: int