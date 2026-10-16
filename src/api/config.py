"""Shared paths and settings for the PIPS API."""

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
DATA_DIR = PROJECT_ROOT / "data"
GIS_DIR = DATA_DIR / "gis"
EXAM_DIR = DATA_DIR / "exam"
OUTPUT_DIR = PROJECT_ROOT / "output"

API_TITLE = "PIPS API"
API_VERSION = "0.1.0"
API_DESCRIPTION = (
    "REST backend for the Predictive Infrastructure Planning System. "
    "Campus mapping, demand scenarios, capacity monitoring, walking access, "
    "and basic facility siting backed by local datasets."
)

CORS_ORIGINS = ["*"]


def first_existing(*paths):
    for path in paths:
        if path.exists():
            return path
    return paths[0]


BUILDINGS_FILE = first_existing(
    GIS_DIR / "buildings.geojson",
    GIS_DIR / "sample_buildings.geojson",
)
PATHS_FILE = first_existing(
    GIS_DIR / "paths.geojson",
    GIS_DIR / "sample_paths.geojson",
)
GRAPH_FILE = OUTPUT_DIR / "campus_graph.graphml"
DISTANCES_FILE = OUTPUT_DIR / "building_distances.json"
EXAM_FILE = first_existing(
    EXAM_DIR / "entrance_exam_history.csv",
    EXAM_DIR / "sample_entrance_exam_history.csv",
)
