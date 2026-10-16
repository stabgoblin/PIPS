"""Planning overview and module navigation."""
import streamlit as st
import api_client
from components.layout import page_header, show_result

MODULES = [
    ("Campus Mapping", "Explore building footprints, paths and the campus network."),
    ("Student Demand Forecasting", "Compare course trends and future demand scenarios."),
    ("Capacity & Threshold Monitoring", "Review facility inventory and occupancy alerts."),
    ("Campus Accessibility", "Find reachable buildings and gaps in the walking network."),
    ("Facility Location Optimization", "Compare eligible parcels using walking distances."),
]


def open_module(name):
    st.session_state["navigation"] = name


def render():
    page_header("Campus planning overview", "A shared view of demand, infrastructure and access.")
    health = api_client.get("/api/health")
    if health.get("status") != "ok":
        show_result(health)
        return
    buildings = api_client.get("/api/mapping/buildings/summary")
    courses = api_client.get("/api/forecast/courses")
    graph = api_client.get("/api/mapping/graph/summary")
    cols = st.columns(3)
    cols[0].metric("Mapped buildings & parcels", len(buildings["data"]) if buildings.get("status") == "ok" else "Unavailable")
    cols[1].metric("Programmes", len(courses["data"]["courses"]) if courses.get("status") == "ok" else "Unavailable")
    cols[2].metric("Network components", graph["data"]["components"] if graph.get("status") == "ok" else "Not built")
    st.caption("Included GIS layers and entrance history are demonstration data. Replace them with verified campus records for planning.")
    st.subheader("Planning workspace")
    for offset in range(0, len(MODULES), 2):
        for column, (name, description) in zip(st.columns(2), MODULES[offset:offset + 2]):
            with column, st.container(border=True):
                st.subheader(name)
                st.write(description)
                st.button("Open module", key=f"open_{name}", on_click=open_module, args=(name,))
