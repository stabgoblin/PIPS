"""Entry point for the PIPS REST API.

Run from the project root with:
    uvicorn src.api.main:app --reload
Interactive docs are then available at http://127.0.0.1:8000/docs
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import API_DESCRIPTION, API_TITLE, API_VERSION, CORS_ORIGINS
from .routers import (
    accessibility,
    campus_mapping,
    capacity_monitor,
    demand_forecast,
    facility_optimizer,
)

app = FastAPI(title=API_TITLE, description=API_DESCRIPTION, version=API_VERSION)

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(campus_mapping.router)
app.include_router(demand_forecast.router)
app.include_router(capacity_monitor.router)
app.include_router(accessibility.router)
app.include_router(facility_optimizer.router)


@app.get("/", tags=["Meta"])
def root():
    return {
        "name": API_TITLE,
        "version": API_VERSION,
        "docs": "/docs",
        "modules": [
            "campus-mapping",
            "student-demand-forecasting",
            "capacity-and-threshold-monitoring",
            "campus-accessibility",
            "facility-location-optimization",
        ],
    }


@app.get("/api/health", tags=["Meta"])
def health():
    return {
        "status": "ok",
        "message": "PIPS API is running",
        "data": {"version": API_VERSION},
    }
