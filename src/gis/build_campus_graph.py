"""
Phase 1: Build Campus Walkable Network Graph
Loads digitized GeoJSON files from QGIS and creates a NetworkX graph.
Each node = intersection/building entrance, edge = walkable path with distance.
"""
import json
import networkx as nx
import geopandas as gpd
from shapely.geometry import Point, LineString, Polygon
from pathlib import Path
import math

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
DATA_DIR = PROJECT_ROOT / "data" / "gis"
OUTPUT_DIR = PROJECT_ROOT / "output"


def load_geojson(filename):
    filepath = DATA_DIR / filename
    if not filepath.exists():
        sample_path = DATA_DIR / f"sample_{filename}"
        if sample_path.exists():
            filepath = sample_path
        else:
            raise FileNotFoundError(f"Missing: {filepath}\nDigitize this layer in QGIS first.")
    return gpd.read_file(filepath)


def haversine_meters(coord1, coord2):
    """Calculate distance in meters between two (lon, lat) points."""
    R = 6371000
    lon1, lat1 = math.radians(coord1[0]), math.radians(coord1[1])
    lon2, lat2 = math.radians(coord2[0]), math.radians(coord2[1])
    dlat, dlon = lat2 - lat1, lon2 - lon1
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def get_polygons_centroid(geojson_file, name_col="name"):
    gdf = load_geojson(geojson_file)
    centroids = []
    for _, row in gdf.iterrows():
        geom = row.geometry
        if isinstance(geom, Polygon):
            c = geom.centroid
        elif isinstance(geom, Point):
            c = geom
        else:
            continue
        name = row.get(name_col, f"building_{len(centroids)}")
        centroids.append({
            "name": name,
            "type": row.get("type", "unknown"),
            "zone": row.get("zone", "general"),
            "capacity": row.get("capacity", 0),
            "centroid": (c.x, c.y),
            "geometry": geom
        })
    return centroids


def build_graph(buildings_file="buildings.geojson", paths_file="paths.geojson"):
    G = nx.Graph()

    buildings = get_polygons_centroid(buildings_file)
    for b in buildings:
        G.add_node(
            b["name"],
            pos=f"{b['centroid'][0]},{b['centroid'][1]}",
            btype=b["type"],
            zone=b["zone"],
            capacity=b["capacity"],
            node_type="building"
        )
    print(f"Added {len(buildings)} building nodes")

    paths_gdf = load_geojson(paths_file)
    edge_count = 0
    for _, row in paths_gdf.iterrows():
        geom = row.geometry
        if not isinstance(geom, LineString):
            continue
        coords = list(geom.coords)
        path_name = row.get("name", f"path_{edge_count}")
        path_type = row.get("type", "walkway")

        for i in range(len(coords) - 1):
            # Shared coordinates must identify the same junction across paths.
            n1 = f"junction_{coords[i][0]:.7f}_{coords[i][1]:.7f}"
            n2 = f"junction_{coords[i + 1][0]:.7f}_{coords[i + 1][1]:.7f}"
            dist = haversine_meters(coords[i], coords[i + 1])

            if i == 0:
                for b in buildings:
                    bdist = haversine_meters(coords[0], b["centroid"])
                    if bdist < 50:
                        G.add_edge(b["name"], n1, weight=bdist, edge_type="access")
            if i == len(coords) - 2:
                for b in buildings:
                    bdist = haversine_meters(coords[-1], b["centroid"])
                    if bdist < 50:
                        G.add_edge(b["name"], n2, weight=bdist, edge_type="access")

            G.add_node(n1, pos=f"{coords[i][0]},{coords[i][1]}", node_type="junction")
            G.add_node(n2, pos=f"{coords[i + 1][0]},{coords[i + 1][1]}", node_type="junction")
            G.add_edge(n1, n2, weight=dist, edge_type=path_type)
            edge_count += 1

    print(f"Added {edge_count} path edges")
    return G


def print_graph_stats(G):
    print(f"\n--- Campus Graph Stats ---")
    print(f"Nodes: {G.number_of_nodes()}")
    print(f"Edges: {G.number_of_edges()}")
    print(f"Components: {nx.number_connected_components(G)}")
    buildings = [n for n, d in G.nodes(data=True) if d.get("node_type") == "building"]
    print(f"Buildings: {len(buildings)}")
    for b in buildings:
        neighbors = list(G.neighbors(b))
        print(f"  {b}: {len(neighbors)} connections")


def compute_all_pairs_distance(G):
    buildings = [n for n, d in G.nodes(data=True) if d.get("node_type") == "building"]
    dist_dict = {}
    for source in buildings:
        lengths = nx.single_source_dijkstra_path_length(G, source, weight="weight")
        dist_dict[source] = {t: round(l, 1) for t, l in lengths.items() if t in buildings}
    return dist_dict


def main():
    print("=== Building Campus Graph ===\n")
    G = build_graph()
    print_graph_stats(G)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    nx.write_graphml(G, str(OUTPUT_DIR / "campus_graph.graphml"))
    print(f"\nSaved graph to {OUTPUT_DIR / 'campus_graph.graphml'}")

    distances = compute_all_pairs_distance(G)
    with open(OUTPUT_DIR / "building_distances.json", "w") as f:
        json.dump(distances, f, indent=2)
    print(f"Saved distance matrix to {OUTPUT_DIR / 'building_distances.json'}")


if __name__ == "__main__":
    main()
