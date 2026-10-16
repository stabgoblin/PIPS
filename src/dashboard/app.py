"""Streamlit dashboard for the Predictive Infrastructure Planning System.

Run from the project root with:
    streamlit run src/dashboard/app.py
The API should be running separately (see src/api/main.py).
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import streamlit as st

from components.layout import apply_theme
from views import (
    accessibility,
    api_status,
    campus_mapping,
    capacity_monitor,
    demand_forecast,
    facility_optimizer,
    home,
)

st.set_page_config(page_title="PIPS Dashboard", page_icon=":bar_chart:", layout="wide")

PAGES = {
    "Home": home.render,
    "Campus Mapping": campus_mapping.render,
    "Student Demand Forecasting": demand_forecast.render,
    "Capacity & Threshold Monitoring": capacity_monitor.render,
    "Campus Accessibility": accessibility.render,
    "Facility Location Optimization": facility_optimizer.render,
    "API Status": api_status.render,
}

NAVIGATION = [
    ("Home", "Overview", ":material/dashboard:"),
    ("Campus Mapping", "Campus map", ":material/map:"),
    ("Student Demand Forecasting", "Demand", ":material/trending_up:"),
    ("Capacity & Threshold Monitoring", "Capacity", ":material/donut_large:"),
    ("Campus Accessibility", "Accessibility", ":material/directions_walk:"),
    ("Facility Location Optimization", "Site planning", ":material/add_location_alt:"),
]


def navigate(page):
    st.session_state["navigation"] = page


def main():
    apply_theme()
    choice = st.session_state.get("navigation", "Home")
    if choice not in PAGES:
        choice = "Home"
        st.session_state["navigation"] = choice
    with st.container(key="workspace_header"):
        brand, settings = st.columns([5, 1], vertical_alignment="center")
        with brand:
            st.markdown('<div class="pips-brand"><span class="pips-logo">P</span>'
                        '<div><strong>PIPS</strong><span class="pips-tagline">Campus planning workspace</span></div></div>',
                        unsafe_allow_html=True)
        with settings:
            st.button("System", icon=":material/settings:", key="nav_system",
                      type="primary" if choice == "API Status" else "tertiary",
                      on_click=navigate, args=("API Status",), width="stretch")
    with st.container(key="module_navigation"):
        for column, (page, label, icon) in zip(st.columns(len(NAVIGATION), gap="small"), NAVIGATION):
            with column:
                st.button(label, icon=icon, key=f"nav_{page}", width="stretch",
                          type="primary" if choice == page else "secondary",
                          on_click=navigate, args=(page,))
    PAGES[choice]()


if __name__ == "__main__":
    main()
