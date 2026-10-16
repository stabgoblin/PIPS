"""Folium map builders used by the dashboard views."""

import folium
from html import escape
from shapely.geometry import Polygon
from streamlit_folium import st_folium

BUILDING_COLORS = {
    "academic": "blue",
    "hostel_boys": "green",
    "hostel_girls": "purple",
    "mess": "orange",
    "admin": "red",
    "sports": "darkred",
    "library": "cadetblue",
    "parking": "gray",
    "open_land": "beige",
    "candidate_site": "darkgreen",
}

DEFAULT_CENTER = [28.5685, 77.1245]


def _polygon_centroid(coords):
    ring = coords[0] if coords else []
    if not ring:
        return None
    center = Polygon(ring, coords[1:]).centroid
    return [center.y, center.x]


def render_campus_map(buildings_geojson=None, paths_geojson=None, center=None, zoom=16, height=480):
    map_center = center or DEFAULT_CENTER
    campus_map = folium.Map(location=map_center, zoom_start=zoom, tiles="OpenStreetMap")

    if paths_geojson:
        for feature in paths_geojson.get("features", []):
            coords = feature.get("geometry", {}).get("coordinates", [])
            line = [[point[1], point[0]] for point in coords]
            if line:
                folium.PolyLine(
                    line, color="#3b6fb6", weight=3, opacity=0.7, tooltip=feature.get("properties", {}).get("name")
                ).add_to(campus_map)

    if buildings_geojson:
        folium.GeoJson(
            buildings_geojson, name="Building footprints",
            style_function=lambda feature: {"color": "#176b78", "weight": 2,
                "fillColor": "#80c4b7", "fillOpacity": 0.3},
        ).add_to(campus_map)
        for feature in buildings_geojson.get("features", []):
            props = feature.get("properties", {})
            geometry = feature.get("geometry", {})
            if geometry.get("type") != "Polygon":
                continue
            point = _polygon_centroid(geometry.get("coordinates"))
            if point is None:
                continue
            color = BUILDING_COLORS.get(props.get("type"), "blue")
            popup = (
                f"<b>{escape(str(props.get('name', 'Unnamed')))}</b><br>"
                f"Type: {escape(str(props.get('type', 'n/a')))}<br>"
                f"Zone: {escape(str(props.get('zone', 'n/a')))}<br>"
                f"Capacity: {escape(str(props.get('capacity', 'n/a')))}"
            )
            folium.Marker(
                location=point,
                tooltip=props.get("name", "building"),
                popup=folium.Popup(popup, max_width=250),
                icon=folium.Icon(color=color, icon="building", prefix="fa"),
            ).add_to(campus_map)

    return st_folium(campus_map, height=height, use_container_width=True)
