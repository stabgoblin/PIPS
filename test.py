import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt

# Configure OSMnx settings and use an alternative Overpass mirror to bypass 504 timeouts
ox.settings.use_cache = True
ox.settings.log_console = True
ox.settings.overpass_endpoint = "https://lz4.overpass-api.de/api/interpreter"
ox.settings.timeout = 180  # Give it up to 3 minutes if needed

def fetch_nit_trichy_campus():
    # Geographic boundaries for NIT Trichy
    NORTH = 10.7720
    SOUTH = 10.7550
    EAST = 78.8260
    WEST = 78.8080
    
    bbox = (WEST, SOUTH, EAST, NORTH)
    
    print("Fetching NIT Trichy walkable street network from alternative OpenStreetMap mirror...")
    # 1. Download pedestrian/walkable path network graph
    G = ox.graph_from_bbox(
        bbox, 
        network_type='walk', 
        simplify=True
    )
    
    # 2. Project the graph to a local UTM zone so edge weights are measured in exact meters
    G_projected = ox.project_graph(G)
    
    print("Fetching NIT Trichy building footprints...")
    try:
        buildings = ox.features_from_bbox(
            bbox, 
            tags={'building': True}
        )
    except AttributeError:
        buildings = ox.geometries_from_bbox(
            bbox, 
            tags={'building': True}
        )
        
    return G_projected, buildings

if __name__ == "__main__":
    campus_graph, campus_buildings = fetch_nit_trichy_campus()
    
    print("\nExtraction Successful!")
    print(f"- Walkable Graph Nodes: {campus_graph.number_of_nodes()}")
    print(f"- Walkable Graph Edges: {campus_graph.number_of_edges()}")
    print(f"- Building Footprints Mapped: {len(campus_buildings) if campus_buildings is not None else 0}")
    
    fig, ax = ox.plot_graph(
        campus_graph, 
        show=False, 
        close=False, 
        node_size=8, 
        node_color='#1f77b4', 
        edge_color='#888888', 
        edge_linewidth=0.8
    )
    
    if campus_buildings is not None and not campus_buildings.empty:
        campus_buildings.plot(ax=ax, facecolor='#ff7f0e', edgecolor='#111111', alpha=0.6)
        
    plt.title("NIT Trichy Campus — Automated Walkability Graph & Buildings", fontsize=13, fontweight='bold')
    plt.tight_layout()
    plt.show()
