"""Capacity inventory with configurable alert thresholds."""
import pandas as pd
import streamlit as st
import api_client
from components.layout import page_header, show_result


def render():
    page_header("Capacity & thresholds", "Track recorded occupancy against each facility's physical capacity.")
    result = api_client.get("/api/capacity/facilities")
    if result.get("status") != "ok":
        show_result(result)
        return
    rows = result["data"]["facilities"]
    if not rows:
        st.info("No facilities available. Add buildings to the GIS inventory.")
        return
    unknown = sum(row["utilization"] is None for row in rows)
    cols = st.columns(3)
    cols[0].metric("Facilities", len(rows))
    cols[1].metric("Threshold alerts", sum(row["status"] == "alert" for row in rows))
    cols[2].metric("Missing occupancy", unknown)
    if unknown:
        st.info("Occupancy is not recorded for some facilities. Add an occupancy property to the building data to calculate utilization.")
    frame = pd.DataFrame(rows).rename(columns={"name": "Facility", "type": "Type", "capacity": "Capacity",
        "occupancy": "Occupancy", "utilization": "Utilization", "threshold": "Threshold", "status": "Status"})
    for column in ("Utilization", "Threshold"):
        frame[column] = frame[column].map(lambda value: f"{value:.0%}" if pd.notna(value) else "Unknown")
    st.dataframe(frame, use_container_width=True, hide_index=True)
    rules = api_client.get("/api/capacity/thresholds")
    if rules.get("status") != "ok":
        show_result(rules)
        return
    st.subheader("Alert settings")
    scope = st.selectbox("Apply to", ["All facility types"] + sorted({row["type"] for row in rows}))
    facility_type = None if scope == "All facility types" else scope
    data = rules["data"]
    current = data["overrides"].get(facility_type, data["default_threshold"])
    with st.form("thresholds"):
        threshold = st.slider("Utilization threshold (%)", 0, 100, round(current * 100), key=f"threshold_{scope}")
        st.caption("An alert triggers at or above the threshold. Type-specific settings override the default.")
        if st.form_submit_button("Save threshold", type="primary"):
            response = api_client.post("/api/capacity/thresholds", {"threshold": threshold / 100, "facility_type": facility_type})
            if response.get("status") == "ok":
                st.rerun()
            show_result(response)
