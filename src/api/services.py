"""Shared local data access and planning calculations."""
import json
import os
import tempfile
from threading import RLock

from .config import BUILDINGS_FILE, OUTPUT_DIR
from .utils import load_json

STATE_LOCK = RLock()
THRESHOLDS_FILE = OUTPUT_DIR / "thresholds.json"
RESULTS_FILE = OUTPUT_DIR / "optimization_results.json"
PARCEL_TYPES = {"open_land", "candidate_site"}


def save_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    with STATE_LOCK:
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=path.parent,
                                         suffix=".json", delete=False) as handle:
            temporary = handle.name
            json.dump(data, handle, indent=2, allow_nan=False)
        try:
            os.replace(temporary, path)
        finally:
            if os.path.exists(temporary):
                os.unlink(temporary)


def building_features():
    data = load_json(BUILDINGS_FILE)
    return data.get("features", []) if data else []


def candidates():
    return [dict(feature["properties"], id=feature["properties"]["name"])
            for feature in building_features()
            if feature.get("properties", {}).get("type") in PARCEL_TYPES]


def thresholds():
    return load_json(THRESHOLDS_FILE) or {"default_threshold": 0.85, "overrides": {}}


def facilities():
    rules = thresholds()
    rows = []
    for feature in building_features():
        props = feature.get("properties", {})
        if props.get("type") in PARCEL_TYPES:
            continue
        capacity = props.get("capacity", 0) or 0
        occupancy = props.get("occupancy")
        threshold = rules["overrides"].get(props.get("type"), rules["default_threshold"])
        ratio = occupancy / capacity if occupancy is not None and capacity > 0 else None
        rows.append({"name": props.get("name"), "type": props.get("type"),
                     "capacity": capacity, "occupancy": occupancy,
                     "utilization": ratio, "threshold": threshold,
                     "status": "unknown" if ratio is None else
                     "alert" if ratio >= threshold else "within_threshold"})
    return rows
