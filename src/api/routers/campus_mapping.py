"""Campus mapping endpoints.

Module 1 - GIS & campus network base layer. Building and path layers are
served from data/gis so the dashboard has real data immediately; replace the
reserved endpoints as more digitized layers become available.
"""

import networkx as nx
from fastapi import APIRouter, HTTPException

from ..config import BUILDINGS_FILE, GRAPH_FILE, PATHS_FILE
from ..utils import load_json, ok, pending
from ..services import building_features, PARCEL_TYPES
from shapely.geometry import Polygon

router = APIRouter(prefix="/api/mapping", tags=["Campus Mapping"])


def _require_json(path, label):
    data = load_json(path)
    if data is None:
        raise HTTPException(status_code=404, detail=f"{label} layer not found: {path.name}")
    return data


def _centroid(coords):
    if not coords or not coords[0]:
        return None
    center = Polygon(coords[0], coords[1:]).centroid
    return [round(center.x, 6), round(center.y, 6)]


@router.get("/buildings")
def get_buildings():
    return ok("Building footprints loaded", _require_json(BUILDINGS_FILE, "Buildings"))


@router.get("/paths")
def get_paths():
    return ok("Walkable paths loaded", _require_json(PATHS_FILE, "Paths"))


@router.get("/buildings/summary")
def get_buildings_summary():
    geo = _require_json(BUILDINGS_FILE, "Buildings")
    items = []
    for feature in geo.get("features", []):
        props = feature.get("properties", {})
        geometry = feature.get("geometry", {})
        center = None
        if geometry.get("type") == "Polygon":
            center = _centroid(geometry.get("coordinates"))
        items.append(
            {
                "name": props.get("name"),
                "type": props.get("type"),
                "zone": props.get("zone"),
                "capacity": props.get("capacity"),
                "center": center,
            }
        )
    return ok(f"{len(items)} buildings", items)


@router.get("/center")
def get_center():
    geo = _require_json(BUILDINGS_FILE, "Buildings")
    points = [
        center
        for center in (
            _centroid(feature.get("geometry", {}).get("coordinates"))
            for feature in geo.get("features", [])
            if feature.get("geometry", {}).get("type") == "Polygon"
        )
        if center
    ]
    if not points:
        return pending("No building centroids available yet", {"lat": None, "lon": None})
    lon = sum(point[0] for point in points) / len(points)
    lat = sum(point[1] for point in points) / len(points)
    return ok("Campus centre", {"lat": round(lat, 6), "lon": round(lon, 6)})


@router.get("/graph/summary")
def get_graph_summary():
    if not GRAPH_FILE.exists():
        return pending(
            "Campus graph not built yet. Run src/gis/build_campus_graph.py once your layers are exported.",
            {"nodes": 0, "edges": 0, "components": 0, "buildings": 0},
        )
    try:
        graph = nx.read_graphml(str(GRAPH_FILE))
    except Exception as exc:
        return pending(f"Could not read campus graph: {exc}", {"graph_file": GRAPH_FILE.name})

    buildings = [
        node for node, data in graph.nodes(data=True) if data.get("node_type") == "building"
    ]
    return ok(
        "Campus graph summary",
        {
            "nodes": graph.number_of_nodes(),
            "edges": graph.number_of_edges(),
            "components": nx.number_connected_components(graph),
            "buildings": len(buildings),
            "graph_file": GRAPH_FILE.name,
        },
    )


@router.get("/graph/nodes")
def get_graph_nodes():
    if not GRAPH_FILE.exists():
        return pending("Build the campus graph first.", {"nodes": []})
    graph = nx.read_graphml(GRAPH_FILE)
    nodes = []
    for name, attributes in graph.nodes(data=True):
        lon, lat = map(float, attributes["pos"].split(","))
        nodes.append({"id": name, "lon": lon, "lat": lat, **attributes})
    return ok("Campus network nodes", {"nodes": nodes})


@router.get("/parcels")
def get_parcels():
    return ok("Candidate parcel features", {"parcels": [feature for feature in building_features()
        if feature.get("properties", {}).get("type") in PARCEL_TYPES]})
