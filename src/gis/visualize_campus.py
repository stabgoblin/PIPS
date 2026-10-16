"""
Visualize the campus graph on an interactive Leaflet map using Folium.
Generates an HTML file you can open in a browser.
"""
import json
import networkx as nx
import folium
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
OUTPUT_DIR = PROJECT_ROOT / "output"
DATA_DIR = PROJECT_ROOT / "data" / "gis"

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


def load_graph():
    graphml = OUTPUT_DIR / "campus_graph.graphml"
    if not graphml.exists():
        raise FileNotFoundError("Run build_campus_graph.py first.")
    return nx.read_graphml(graphml)


def _parse_pos(p):
    if isinstance(p, str):
        parts = [float(x) for x in p.split(",")]
        return parts[0], parts[1]
    return float(p[0]), float(p[1])


def get_center(G):
    positions = nx.get_node_attributes(G, "pos")
    lats = [_parse_pos(p)[1] for p in positions.values() if p]
    lons = [_parse_pos(p)[0] for p in positions.values() if p]
    return (sum(lats) / len(lats), sum(lons) / len(lons)) if lats else (0, 0)


def visualize():
    G = load_graph()
    center = get_center(G)
    m = folium.Map(location=center, zoom_start=17, tiles="OpenStreetMap")

    buildings = {n: d for n, d in G.nodes(data=True) if d.get("node_type") == "building"}
    for name, data in buildings.items():
        pos = data.get("pos")
        if not pos:
            continue
        lon, lat = _parse_pos(pos)
        btype = data.get("btype", "unknown")
        color = BUILDING_COLORS.get(btype, "blue")
        capacity = data.get("capacity", "N/A")

        popup_html = f"""
        <b>{name}</b><br>
        Type: {btype}<br>
        Zone: {data.get('zone', 'N/A')}<br>
        Capacity: {capacity}
        """
        folium.Marker(
            location=[lat, lon],
            popup=folium.Popup(popup_html, max_width=250),
            tooltip=name,
            icon=folium.Icon(color=color, icon="building", prefix="fa"),
        ).add_to(m)

    edges = [(u, v) for u, v, d in G.edges(data=True) if d.get("edge_type") != "access"]
    for u, v in edges:
        pos_u = G.nodes[u].get("pos")
        pos_v = G.nodes[v].get("pos")
        if pos_u and pos_v:
            lon_u, lat_u = _parse_pos(pos_u)
            lon_v, lat_v = _parse_pos(pos_v)
            coords = [
                [lat_u, lon_u],
                [lat_v, lon_v],
            ]
            folium.PolyLine(coords, color="blue", weight=2, opacity=0.6).add_to(m)

    m.save(str(OUTPUT_DIR / "campus_map.html"))
    print(f"Map saved to {OUTPUT_DIR / 'campus_map.html'}")
    print("Open this file in a browser to view your campus map.")


if __name__ == "__main__":
    visualize()
