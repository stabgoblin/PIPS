"""Campus mapping page."""

import streamlit as st

import api_client
from components.layout import page_header
from components.maps import render_campus_map


def render():
    page_header("Campus Mapping", "Digitized building footprints and walkable paths")

    buildings = api_client.get("/api/mapping/buildings")
    if buildings.get("status") != "ok":
        st.warning(buildings.get("message"))
        return

    paths = api_client.get("/api/mapping/paths")
    center = None
    center_result = api_client.get("/api/mapping/center")
    if center_result.get("status") == "ok":
        data = center_result["data"]
        center = [data["lat"], data["lon"]]

    building_geo = buildings["data"]
    path_geo = paths["data"] if paths.get("status") == "ok" else None
    render_campus_map(building_geo, path_geo, center=center)

    summary = api_client.get("/api/mapping/buildings/summary")
    if summary.get("status") == "ok":
        st.subheader("Buildings")
        rows = [
            {
                "Name": building.get("name"),
                "Type": building.get("type"),
                "Zone": building.get("zone"),
                "Capacity": building.get("capacity"),
            }
            for building in summary["data"]
        ]
        st.dataframe(rows, use_container_width=True)

    graph = api_client.get("/api/mapping/graph/summary")
    if graph.get("status") == "ok":
        data = graph["data"]
        st.subheader("Campus graph")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Nodes", data.get("nodes"))
        col2.metric("Edges", data.get("edges"))
        col3.metric("Components", data.get("components"))
        col4.metric("Buildings", data.get("buildings"))
    else:
        st.info(graph.get("message"))
