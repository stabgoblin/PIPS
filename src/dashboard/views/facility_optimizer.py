"""Facility siting controls and readable solver results."""
import streamlit as st
import api_client
from components.layout import page_header, show_result

FACILITY_TYPES = ["hostel_boys", "hostel_girls", "academic", "mess", "sports", "library"]


def render():
    page_header("Facility location planning", "Choose sites that minimize capacity-weighted walking distance.")
    result = api_client.get("/api/optimization/candidates")
    if result.get("status") != "ok":
        show_result(result)
        return
    sites = result["data"]["candidates"]
    if not sites:
        st.info("Add open_land or candidate_site parcels to the building layer to begin.")
        return
    st.subheader("Available parcels")
    st.dataframe(sites, use_container_width=True, hide_index=True)
    with st.form("pmedian_form"):
        left, right = st.columns(2)
        p = left.number_input("Facilities to add", min_value=1, max_value=len(sites), value=1)
        facility_type = right.selectbox("Facility type", FACILITY_TYPES, format_func=lambda value: value.replace("_", " ").title())
        candidates = st.multiselect("Candidate parcels", [site["id"] for site in sites], default=[site["id"] for site in sites])
        respect_zoning = st.checkbox("Apply basic zone eligibility", value=True)
        st.caption("Uses physical capacity as the demand weight. All demand buildings must have a route to a selected site.")
        submitted = st.form_submit_button("Compare locations", type="primary")
    if submitted:
        with st.spinner("Comparing eligible locations..."):
            st.session_state["optimizer_result"] = api_client.post("/api/optimization/pmedian", {
                "p": int(p), "facility_type": facility_type, "respect_zoning": respect_zoning, "candidate_ids": candidates})
    if "optimizer_result" in st.session_state:
        response = st.session_state["optimizer_result"]
        show_result(response)
        if response.get("status") == "ok":
            data = response["data"]
            st.caption("Last submitted scenario; submit again after changing settings.")
            st.metric("Weighted average walk", f"{data['average_distance_m']:,.1f} m")
            st.subheader("Recommended sites")
            st.dataframe(data["selected"], hide_index=True, use_container_width=True)
            st.subheader("Building assignments")
            st.dataframe(data["assignments"], hide_index=True, use_container_width=True)
