"""Reachability on the exported walking network."""
from fastapi import APIRouter, HTTPException, Query
from ..config import DISTANCES_FILE
from ..utils import load_json, ok, pending

router = APIRouter(prefix="/api/accessibility", tags=["Campus Accessibility"])

@router.get("/matrix")
def distance_matrix():
    data = load_json(DISTANCES_FILE)
    if data is None:
        return pending("Build the campus network to calculate walking distances.", {})
    return ok("Walking distances in metres; missing destinations are unreachable", data)

@router.get("/from/{building}")
def reachability_from(building: str):
    result = distance_matrix()
    if result["status"] != "ok":
        return result
    if building not in result["data"]:
        raise HTTPException(404, "Building not found in walking network")
    return ok(f"Walking distances from {building}", result["data"][building])

@router.get("/unreachable")
def unreachable_pairs():
    result = distance_matrix()
    if result["status"] != "ok":
        return result
    data = result["data"]
    names = sorted(data)
    gaps = [{"from": source, "to": target} for i, source in enumerate(names)
            for target in names[i + 1:] if target not in data[source]]
    return ok("Disconnected building pairs", {"gaps": gaps})

@router.get("/isochrones")
def isochrones(building: str, minutes: float = Query(5, gt=0, le=120),
               speed_m_per_min: float = Query(80, gt=0, le=200)):
    result = reachability_from(building)
    if result["status"] != "ok":
        return result
    reachable = [{"building": name, "distance_m": distance,
                  "minutes": round(distance / speed_m_per_min, 2)}
                 for name, distance in result["data"].items()
                 if distance <= minutes * speed_m_per_min]
    return ok("Network service area (reachable buildings, not a polygon)", {
        "origin": building, "minutes": minutes, "reachable": reachable})
