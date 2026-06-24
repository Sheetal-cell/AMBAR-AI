from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.api.aqi import router as aqi_router
from backend.api.hotspots import router as hotspot_router
from backend.api.fire import router as fire_router

app = FastAPI(
    title="AMBAR AI",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    aqi_router,
    prefix="/api/aqi",
    tags=["AQI"]
)

app.include_router(
    hotspot_router,
    prefix="/api/hotspots",
    tags=["HCHO"]
)

app.include_router(
    fire_router,
    prefix="/api/fire",
    tags=["Fire"]
)


@app.get("/")
def root():
    return {
        "project": "AMBAR AI",
        "status": "running"
    }