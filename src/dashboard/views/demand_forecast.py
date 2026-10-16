"""Student demand forecasting page (Module 2).

Provides interactive predictive modeling, historical JoSAA/entrance applicant trends,
cutoff rank trajectory, and capacity expansion recommendations for NIT Trichy courses.
"""

import pandas as pd
import streamlit as st

import api_client
from components.layout import page_header, show_result


def render():
    page_header(
        "Student Demand Forecasting",
        "Predict seat demand, applicant selectivity, and required infrastructure per course",
    )

    st.info("Demonstration dataset: synthetic course history. Forecast ranges and seat suggestions are illustrative planning heuristics.")

    # 1. Fetch available courses from API
    courses_resp = api_client.get("/api/forecast/courses")
    courses_data = []
    if courses_resp.get("status") == "ok" and courses_resp.get("data"):
        courses_data = courses_resp["data"].get("courses", [])

    if not courses_data:
        show_result(courses_resp)
        st.info("No courses are available. Check the dataset and API connection.")
        return

    # Build dropdown options
    course_options = {
        f"{c['course_id']} - {c['course_name']}": c["course_id"]
        for c in courses_data
    }
    course_keys = list(course_options.keys())

    # 2. Top-level parameters in 3 columns
    col_sel1, col_sel2, col_sel3 = st.columns([2, 1, 1])
    with col_sel1:
        selected_label = st.selectbox("Select Engineering Programme", course_keys, index=0)
        selected_course = course_options[selected_label]
    with col_sel2:
        horizon = st.slider("Forecast Horizon (Years)", min_value=1, max_value=5, value=3)
    with col_sel3:
        model_choice = st.selectbox(
            "Forecasting Model",
            ["Auto (Best historical fit)", "Polynomial Regression (scikit-learn)", "Holt trend smoothing"],
            index=0,
        )

    model_code = "auto"
    if "Regression" in model_choice:
        model_code = "regression"
    elif "Holt" in model_choice:
        model_code = "holt"

    # Optional scenario adjustment
    with st.expander("Advanced What-If Scenario Settings", expanded=False):
        growth_slider = st.slider(
            "National Applicant Growth Modifier (% annual shift from baseline)",
            min_value=-10,
            max_value=20,
            value=0,
            step=1,
            help="Simulate accelerated national applicant surges (e.g. tech/AI boom) or demographic contraction.",
        )
        growth_multiplier = 1.0 + (growth_slider / 100.0)

    # 3. Call API to generate forecast
    payload = {
        "course_id": selected_course,
        "horizon_years": int(horizon),
        "model_type": model_code,
        "growth_multiplier": growth_multiplier,
    }
    forecast_resp = api_client.post("/api/forecast/predict", payload)

    if forecast_resp.get("status") != "ok" or not forecast_resp.get("data"):
        show_result(forecast_resp)
        return

    data = forecast_resp["data"]
    current_stats = data.get("current_stats", {})
    model_meta = data.get("model_metadata", {})
    insights = data.get("planning_insights", {})
    projections = data.get("projections", [])
    history = data.get("historical_series", [])

    # 4. Highlight Key Metrics (KPIs)
    st.divider()
    m1, m2, m3, m4, m5 = st.columns(5)
    m1.metric(
        "Latest Applicants",
        f"{current_stats.get('applicants', 0):,}",
        f"{model_meta.get('projected_cagr_pct', 0.0)}% CAGR",
    )
    m2.metric(
        "Current Seats",
        f"{current_stats.get('seat_intake', 0)}",
    )
    m3.metric(
        "Acceptance Rate",
        f"{current_stats.get('acceptance_rate_pct', 0.0):.4f}%",
        delta_color="inverse",
    )
    m4.metric(
        "Latest Closing Rank",
        f"{current_stats.get('closing_rank', 0):,}",
    )
    m5.metric(
        "Model Fit (R²)",
        f"{model_meta.get('r2_score', 0.0):.3f}",
        model_meta.get("model_used", "").split("[")[0].strip(),
    )

    # 5. Strategic Recommendation Card
    outlook_color = (
        "success" if insights.get("demand_outlook") == "Surging" else "info"
    )
    st.info(f"**Planning Insight & Recommendation:** {insights.get('recommendation', '')}")

    # 6. Visualizations Tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "📈 Demand Projections",
        "🎯 Selectivity & Cutoffs",
        "🏗️ Capacity Planning",
        "🏛️ Department Overview",
    ])

    with tab1:
        st.subheader("Historical vs Projected Applicant Volume")
        # Build unified DataFrame for chart
        hist_records = [{"Year": h["year"], "Historical Applicants": h["applicants"], "Projected Applicants": None} for h in history]
        # Connect last historical year to projections
        if hist_records:
            hist_records[-1]["Projected Applicants"] = hist_records[-1]["Historical Applicants"]
        for p in projections:
            hist_records.append({
                "Year": p["year"],
                "Historical Applicants": None,
                "Projected Applicants": p["projected_applicants"],
            })
        chart_df = pd.DataFrame(hist_records).set_index("Year")
        st.line_chart(chart_df, color=["#1f77b4", "#ff7f0e"])

        # Table of multi-year forecasts with confidence bounds
        st.markdown("**Multi-year projections (approximate residual-based range)**")
        proj_rows = [
            {
                "Year": p["year"],
                "Projected Applicants": f"{p['projected_applicants']:,}",
                "Approximate lower bound": f"{p['lower_bound']:,}",
                "Approximate upper bound": f"{p['upper_bound']:,}",
                "Demand Index (vs Base)": f"{p['demand_index']:.2f}x",
                "Projected Applicants / Seat": f"{p['projected_applicants_per_seat']:.1f}",
            }
            for p in projections
        ]
        st.dataframe(pd.DataFrame(proj_rows), use_container_width=True)

    with tab2:
        st.subheader("Competitiveness & Cutoff Trajectory")
        col_c1, col_c2 = st.columns(2)

        with col_c1:
            st.markdown("**Closing Rank Trend (Lower = More Competitive)**")
            rank_records = [{"Year": h["year"], "Closing Rank": h["closing_rank"]} for h in history]
            for p in projections:
                rank_records.append({"Year": p["year"], "Closing Rank": p["projected_closing_rank"]})
            rank_df = pd.DataFrame(rank_records).set_index("Year")
            st.line_chart(rank_df, color="#2ca02c")

        with col_c2:
            st.markdown("**Applicants Competing Per Seat**")
            comp_records = [
                {"Year": h["year"], "Applicants Per Seat": round(h["applicants"] / h["intake"], 1)}
                for h in history
            ]
            for p in projections:
                comp_records.append({"Year": p["year"], "Applicants Per Seat": p["projected_applicants_per_seat"]})
            comp_df = pd.DataFrame(comp_records).set_index("Year")
            st.line_chart(comp_df, color="#d62728")

        st.caption(
            "Note: General category JoSAA Other-State / Home-State blended cutoff ranks. "
            "A declining closing rank curve signifies intensifying competition."
        )

    with tab3:
        st.subheader("Seat Intake & Physical Capacity Expansion")
        st.markdown(
            "Comparison of current frozen intake versus algorithmically recommended capacity "
            "to absorb surging student demand while preserving educational standards."
        )

        cap_records = []
        for h in history:
            cap_records.append({
                "Year": h["year"],
                "Sanctioned Intake": h["intake"],
                "Recommended Capacity": h["intake"],
            })
        for p in projections:
            cap_records.append({
                "Year": p["year"],
                "Sanctioned Intake": p["current_seat_intake"],
                "Recommended Capacity": p["recommended_seat_intake"],
            })

        cap_df = pd.DataFrame(cap_records).set_index("Year")
        st.line_chart(cap_df, color=["#7f7f7f", "#1f77b4"])

        # Infrastructure expansion metrics
        if projections:
            last_p = projections[-1]
            diff_seats = last_p["recommended_seat_intake"] - last_p["current_seat_intake"]
            if diff_seats > 0:
                st.success(
                    f"**Proposed Infrastructure Expansion by {last_p['year']}:** "
                    f"+{diff_seats} seats ({last_p['recommended_seat_intake']} total). "
                    f"Validate the seat scenario against actual enrollment, space and staffing."
                )
            else:
                st.info(
                    f"No seat expansion suggested by this heuristic through {last_p['year']}. Confirm with enrollment data."
                )

    with tab4:
        st.subheader("Institution-Wide Department Comparison")
        overview_resp = api_client.get("/api/forecast/overview")
        if overview_resp.get("status") == "ok" and overview_resp.get("data"):
            ov_data = overview_resp["data"]
            st.caption(f"Institute: {ov_data.get('institute', 'NIT Trichy')} | Total Sanctioned Seats: {ov_data.get('total_sanctioned_intake', 0):,}")

            dept_list = ov_data.get("courses", [])
            if dept_list:
                dept_df = pd.DataFrame(dept_list)
                chart_data = dept_df[["course_id", "course_applicants"]].set_index("course_id")
                st.bar_chart(chart_data)

                st.markdown("**Complete Engineering Department Matrix**")
                table_view = dept_df[[
                    "course_id", "course_name", "department", "course_applicants",
                    "preference_share_pct", "sanctioned_intake", "closing_rank",
                    "acceptance_rate_pct", "applicants_per_seat"
                ]].rename(columns={
                    "course_id": "Code",
                    "course_name": "Programme",
                    "department": "Department",
                    "course_applicants": "Applicants",
                    "preference_share_pct": "Preference %",
                    "sanctioned_intake": "Seats",
                    "closing_rank": "Closing Rank",
                    "acceptance_rate_pct": "Acceptance %",
                    "applicants_per_seat": "Applicants/Seat",
                })
                st.dataframe(table_view, use_container_width=True)
        else:
            show_result(overview_resp)

    # 7. Dataset provenance footer
    with st.expander("Dataset Provenance & Ingested Files", expanded=False):
        datasets_resp = api_client.get("/api/forecast/datasets")
        if datasets_resp.get("status") == "ok":
            st.json(datasets_resp.get("data"))
