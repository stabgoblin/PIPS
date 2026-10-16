"""API status page - lists the available endpoints per module."""

import streamlit as st

import api_client
from components.layout import page_header
from settings import API_BASE_URL

ENDPOINTS = {
    "Meta": ["GET /api/health"],
    "Campus Mapping": [
        "GET /api/mapping/buildings",
        "GET /api/mapping/paths",
        "GET /api/mapping/buildings/summary",
        "GET /api/mapping/center",
        "GET /api/mapping/graph/summary",
        "GET /api/mapping/graph/nodes",
        "GET /api/mapping/parcels",
    ],
    "Student Demand Forecasting": [
        "GET /api/forecast/courses",
        "GET /api/forecast/history/{course_id}",
        "POST /api/forecast/predict",
        "GET /api/forecast/datasets",
    ],
    "Capacity & Threshold Monitoring": [
        "GET /api/capacity/facilities",
        "GET /api/capacity/utilization",
        "GET /api/capacity/alerts",
        "GET /api/capacity/thresholds",
        "POST /api/capacity/thresholds",
    ],
    "Campus Accessibility": [
        "GET /api/accessibility/matrix",
        "GET /api/accessibility/from/{building}",
        "GET /api/accessibility/unreachable",
        "GET /api/accessibility/isochrones",
    ],
    "Facility Location Optimization": [
        "GET /api/optimization/candidates",
        "POST /api/optimization/pmedian",
        "GET /api/optimization/results",
    ],
}


def render():
    page_header("API Status", "Connection details and available planning endpoints")

    st.write("Base URL:", API_BASE_URL)
    health = api_client.get("/api/health")
    st.json(health)

    st.divider()
    for group, endpoints in ENDPOINTS.items():
        st.markdown(f"**{group}**")
        st.code("\n".join(endpoints), language="text")

    st.caption("Interactive API docs are available at " + API_BASE_URL + "/docs")

