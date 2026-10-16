"""Walking reachability and connectivity gaps."""
import pandas as pd
import streamlit as st
import api_client
from components.layout import page_header, show_result


def render():
    page_header("Campus accessibility", "Explore walking distances and disconnected parts of campus.")
    result = api_client.get("/api/accessibility/matrix")
    if result.get("status") != "ok":
        show_result(result)
        return
    matrix = result["data"]
    if not matrix:
        st.info("No building distances available. Build the campus network first.")
        return
    left, right = st.columns([2, 1])
    building = left.selectbox("Starting building", sorted(matrix))
    minutes = right.slider("Walking budget (minutes)", 1, 30, 5)
    rows = [{"Destination": name, "Distance (m)": distance,
             "Walk (min)": round(distance / 80, 1), "Within budget": distance <= minutes * 80}
            for name, distance in sorted(matrix[building].items(), key=lambda item: item[1]) if name != building]
    st.caption("Estimated at 80 metres per minute. Route connectivity does not indicate step-free access.")
    if rows:
        st.dataframe(rows, hide_index=True, use_container_width=True)
    else:
        st.warning("This building has no reachable destinations on the current network.")
    missing = sorted(set(matrix) - set(matrix[building]))
    if missing:
        st.warning("No walking route to: " + ", ".join(missing))
    with st.expander("Full distance matrix"):
        st.caption("Distances in metres. Empty cells indicate no connected route.")
        st.dataframe(pd.DataFrame(matrix).T, use_container_width=True)
