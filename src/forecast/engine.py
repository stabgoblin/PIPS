"""Demand Forecasting Engine for Module 2.

Provides historical time-series analytics, course preference tracking,
and multi-year predictive modeling using scikit-learn (Polynomial/Ridge Regression)
and statsmodels (Holt's Linear Trend / ARIMA).
"""

from pathlib import Path
from typing import Any, Dict, List, Optional
import numpy as np
import pandas as pd
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.preprocessing import PolynomialFeatures

try:
    from statsmodels.tsa.holtwinters import ExponentialSmoothing
except ImportError:
    ExponentialSmoothing = None

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
DATA_DIR = PROJECT_ROOT / "data" / "exam"
CSV_PATH = DATA_DIR / "entrance_exam_history.csv"


def load_historical_data() -> pd.DataFrame:
    """Load or generate entrance exam history."""
    if not CSV_PATH.exists():
        from .generate_dummy_data import generate_historical_dataset
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        df = generate_historical_dataset()
        df.to_csv(CSV_PATH, index=False)
        return df
    return pd.read_csv(CSV_PATH)


def get_available_courses() -> List[Dict[str, Any]]:
    """List available courses with latest statistics."""
    df = load_historical_data()
    latest_year = df["year"].max()
    latest_df = df[df["year"] == latest_year]

    courses = []
    for _, row in latest_df.iterrows():
        courses.append({
            "course_id": str(row["course_id"]),
            "course_name": str(row["course_name"]),
            "department": str(row["department"]),
            "latest_year": int(row["year"]),
            "latest_applicants": int(row["course_applicants"]),
            "preference_share_pct": float(row["preference_share_pct"]),
            "sanctioned_intake": int(row["sanctioned_intake"]),
            "closing_rank": int(row["closing_rank"]),
            "acceptance_rate_pct": float(row["acceptance_rate_pct"]),
            "applicants_per_seat": float(row["applicants_per_seat"]),
        })
    return courses


def get_course_history(course_id: str) -> Optional[List[Dict[str, Any]]]:
    """Retrieve full historical records for a specific course."""
    df = load_historical_data()
    course_df = df[df["course_id"].str.upper() == course_id.upper()].sort_values("year")
    if course_df.empty:
        return None

    records = []
    for _, row in course_df.iterrows():
        records.append({
            "year": int(row["year"]),
            "national_exam_applicants": int(row["national_exam_applicants"]),
            "course_applicants": int(row["course_applicants"]),
            "preference_share_pct": float(row["preference_share_pct"]),
            "sanctioned_intake": int(row["sanctioned_intake"]),
            "seats_filled": int(row["seats_filled"]),
            "fill_rate_pct": float(row["fill_rate_pct"]),
            "opening_rank": int(row["opening_rank"]),
            "closing_rank": int(row["closing_rank"]),
            "acceptance_rate_pct": float(row["acceptance_rate_pct"]),
            "applicants_per_seat": float(row["applicants_per_seat"]),
        })
    return records


def get_all_courses_summary() -> Dict[str, Any]:
    """Cross-department overview of applicant volumes and selectivity."""
    df = load_historical_data()
    latest_year = int(df["year"].max())
    latest_df = df[df["year"] == latest_year].sort_values("course_applicants", ascending=False)
    
    total_inst_intake = int(latest_df["sanctioned_intake"].sum())
    total_inst_applicants = int(latest_df["course_applicants"].sum())
    overall_acceptance = round((total_inst_intake / total_inst_applicants) * 100, 3) if total_inst_applicants else 0.0

    return {
        "latest_year": latest_year,
        "institute": "National Institute of Technology, Tiruchirappalli (NIT Trichy)",
        "total_courses": len(latest_df),
        "total_sanctioned_intake": total_inst_intake,
        "total_expressed_preferences": total_inst_applicants,
        "overall_acceptance_rate_pct": overall_acceptance,
        "courses": latest_df[[
            "course_id", "course_name", "department", "course_applicants",
            "preference_share_pct", "sanctioned_intake", "closing_rank",
            "acceptance_rate_pct", "applicants_per_seat"
        ]].to_dict(orient="records"),
    }


def fit_and_forecast_regression(
    years: np.ndarray,
    values: np.ndarray,
    horizon: int,
    degree: int = 1
) -> Dict[str, Any]:
    """Fit polynomial/ridge trend regression and project into the future."""
    X = (years - years[0]).reshape(-1, 1).astype(float)
    y = values.astype(float)

    poly = PolynomialFeatures(degree=degree, include_bias=False)
    X_poly = poly.fit_transform(X)

    model = Ridge(alpha=0.5)
    model.fit(X_poly, y)

    y_pred_hist = model.predict(X_poly)
    r2 = float(r2_score(y, y_pred_hist))
    mae = float(mean_absolute_error(y, y_pred_hist))
    residuals = y - y_pred_hist
    std_resid = float(np.std(residuals)) if len(residuals) > 1 else 0.0

    last_offset = int(years[-1] - years[0])
    future_offsets = np.array([last_offset + i for i in range(1, horizon + 1)]).reshape(-1, 1).astype(float)
    future_X_poly = poly.transform(future_offsets)
    future_preds = model.predict(future_X_poly)

    last_year = int(years[-1])
    forecast_items = []
    for idx, pred_val in enumerate(future_preds):
        f_yr = last_year + idx + 1
        pred_int = max(0, int(round(pred_val)))
        margin = 1.96 * std_resid * np.sqrt(1 + (idx + 1) * 0.25)
        lower = max(0, int(round(pred_val - margin)))
        upper = max(pred_int, int(round(pred_val + margin)))

        forecast_items.append({
            "year": int(f_yr),
            "predicted_value": pred_int,
            "lower_bound": lower,
            "upper_bound": upper,
        })

    return {
        "model_name": f"Polynomial Regression (degree={degree}) [scikit-learn]",
        "r2_score": round(r2, 4),
        "mae": round(mae, 2),
        "std_residual": round(std_resid, 2),
        "forecast": forecast_items,
        "fitted_history": [int(round(v)) for v in y_pred_hist],
    }


def fit_and_forecast_arima(
    years: np.ndarray,
    values: np.ndarray,
    horizon: int
) -> Optional[Dict[str, Any]]:
    """Fit Exponential Smoothing (Holt's Linear Trend) using statsmodels."""
    if ExponentialSmoothing is None or len(values) < 4:
        return None

    try:
        y = values.astype(float)
        # Pass numpy array directly to Holt-Winters to allow integer multi-step forecast
        model = ExponentialSmoothing(
            y,
            trend="add",
            seasonal=None,
            initialization_method="estimated"
        ).fit()

        fitted_values = model.fittedvalues
        r2 = float(r2_score(y, fitted_values))
        mae = float(mean_absolute_error(y, fitted_values))
        residuals = y - fitted_values
        std_resid = float(np.std(residuals)) if len(residuals) > 1 else 0.0

        future_preds = model.forecast(horizon)
        last_year = int(years[-1])

        forecast_items = []
        for idx, pred_val in enumerate(future_preds):
            pred_int = max(0, int(round(pred_val)))
            margin = 1.96 * std_resid * np.sqrt(1 + (idx + 1) * 0.25)
            forecast_items.append({
                "year": last_year + idx + 1,
                "predicted_value": pred_int,
                "lower_bound": max(0, int(round(pred_val - margin))),
                "upper_bound": max(pred_int, int(round(pred_val + margin))),
            })

        return {
            "model_name": "Exponential Smoothing / Holt Linear Trend [statsmodels]",
            "r2_score": round(r2, 4),
            "mae": round(mae, 2),
            "std_residual": round(std_resid, 2),
            "forecast": forecast_items,
            "fitted_history": [int(round(v)) for v in fitted_values],
        }
    except Exception:
        return None


def predict_demand(
    course_id: str,
    horizon_years: int = 3,
    model_type: str = "auto",
    growth_multiplier: float = 1.0,
) -> Dict[str, Any]:
    """Generate multi-year demand forecasts, cutoff projections, and capacity planning."""
    if not 1 <= horizon_years <= 10 or not 0.5 <= growth_multiplier <= 2:
        raise ValueError("Use a horizon of 1-10 years and a growth multiplier of 0.5-2.")
    if model_type not in {"auto", "regression", "regression_linear", "regression_poly", "holt", "arima"}:
        raise ValueError("Unknown forecast model")
    df = load_historical_data()
    course_id = course_id.strip().upper()
    course_df = df[df["course_id"].str.upper() == course_id].sort_values("year")

    if course_df.empty:
        raise ValueError(f"Course '{course_id}' not found in entrance exam dataset.")
    numeric = course_df[["year", "course_applicants", "sanctioned_intake", "closing_rank"]]
    if len(course_df) < 3 or course_df["year"].duplicated().any() or not np.isfinite(numeric.to_numpy(dtype=float)).all() or (numeric <= 0).any().any():
        raise ValueError("Forecasts require at least three unique years with finite positive values.")

    course_name = course_df["course_name"].iloc[0]
    department = course_df["department"].iloc[0]
    years = course_df["year"].values
    applicants = course_df["course_applicants"].values
    intake = course_df["sanctioned_intake"].values
    closing_ranks = course_df["closing_rank"].values

    latest_year = int(years[-1])
    latest_applicants = int(applicants[-1])
    latest_intake = int(intake[-1])
    latest_closing_rank = int(closing_ranks[-1])
    latest_acceptance_pct = round((latest_intake / latest_applicants) * 100, 4)

    # 1. Fit time-series / regression models
    reg_linear = fit_and_forecast_regression(years, applicants, horizon_years, degree=1)
    reg_poly2 = fit_and_forecast_regression(years, applicants, horizon_years, degree=2)
    arima_result = fit_and_forecast_arima(years, applicants, horizon_years)

    # Select best model or respect user request
    if model_type in {"arima", "holt"} and arima_result is None:
        raise ValueError("Holt smoothing is unavailable or there are fewer than four observations.")
    if model_type in {"arima", "holt"} and arima_result is not None:
        chosen_result = arima_result
    elif model_type == "regression_linear":
        chosen_result = reg_linear
    elif model_type == "regression_poly":
        chosen_result = reg_poly2
    elif model_type == "regression":
        chosen_result = reg_poly2 if reg_poly2["r2_score"] > reg_linear["r2_score"] else reg_linear
    else:  # "auto" or default
        candidates = [reg_linear, reg_poly2]
        if arima_result is not None:
            candidates.append(arima_result)
        # Select model with best R2 score
        chosen_result = max(candidates, key=lambda m: m["r2_score"])

    # 2. Fit closing rank trend to project future cutoff competitiveness
    rank_reg = fit_and_forecast_regression(years, closing_ranks, horizon_years, degree=1)

    # 3. Assemble detailed year-by-year projections with infrastructure planning
    projections = []
    base_demand = float(latest_applicants)

    for idx, item in enumerate(chosen_result["forecast"]):
        f_year = item["year"]
        scenario_adj = growth_multiplier ** (idx + 1) - 1.0
        pred_apps = max(100, int(round(item["predicted_value"] * (1.0 + scenario_adj))))
        lower = min(pred_apps, max(0, int(round(item["lower_bound"] * (1.0 + scenario_adj)))))
        upper = max(pred_apps, int(round(item["upper_bound"] * (1.0 + scenario_adj))))

        pred_close_rank = max(100, rank_reg["forecast"][idx]["predicted_value"])
        demand_index = round(pred_apps / base_demand, 3)

        # Recommended seat capacity:
        # If demand grows, recommend an expansion ratio to keep up without lowering bar
        excess_growth = max(0.0, (pred_apps - base_demand) / base_demand)
        recommended_intake = int(round(latest_intake * (1.0 + excess_growth * 0.35)))

        acceptance_at_current = round((latest_intake / pred_apps) * 100, 4) if pred_apps else 0.0
        acceptance_at_recommended = round((recommended_intake / pred_apps) * 100, 4) if pred_apps else 0.0

        projections.append({
            "year": f_year,
            "projected_applicants": pred_apps,
            "lower_bound": lower,
            "upper_bound": upper,
            "demand_index": demand_index,
            "projected_closing_rank": pred_close_rank,
            "current_seat_intake": latest_intake,
            "recommended_seat_intake": recommended_intake,
            "acceptance_rate_current_intake_pct": acceptance_at_current,
            "acceptance_rate_recommended_intake_pct": acceptance_at_recommended,
            "projected_applicants_per_seat": round(pred_apps / latest_intake, 1),
        })

    # CAGR (Compound Annual Growth Rate) of demand over historical period
    cagr_hist = round((((applicants[-1] / applicants[0]) ** (1.0 / (years[-1] - years[0]))) - 1.0) * 100, 2)
    end_proj = projections[-1]["projected_applicants"]
    cagr_proj = round((((end_proj / latest_applicants) ** (1.0 / horizon_years)) - 1.0) * 100, 2)

    # Automated infrastructure recommendation
    if cagr_proj > 5.0:
        recommendation = (
            f"Surging demand detected ({cagr_proj}% CAGR). Student demand for {course_id} is projected to grow "
            f"from {latest_applicants:,} to {end_proj:,} by {projections[-1]['year']}. "
            f"Recommended seat intake expands from {latest_intake} to {projections[-1]['recommended_seat_intake']} seats "
            f"to absorb high-caliber candidates while maintaining quality. "
            f"Validate any expansion against enrollment, staffing and facility requirements."
        )
    elif cagr_proj >= 0.0:
        recommendation = (
            f"Steady demand ({cagr_proj}% CAGR). Current seat intake of {latest_intake} remains well-balanced. "
            f"Maintain existing department facilities while monitoring yearly cutoff shifts."
        )
    else:
        recommendation = (
            f"Stabilizing trend ({cagr_proj}% CAGR). Compare projected applications "
            f"({projections[-1]['projected_applicants']:,} applicants for {latest_intake} seats), "
            f"with actual enrollment before deciding on expansion."
        )

    return {
        "course_id": course_id,
        "course_name": course_name,
        "department": department,
        "base_year": latest_year,
        "current_stats": {
            "applicants": latest_applicants,
            "seat_intake": latest_intake,
            "closing_rank": latest_closing_rank,
            "acceptance_rate_pct": latest_acceptance_pct,
            "historical_cagr_pct": cagr_hist,
        },
        "model_metadata": {
            "model_used": chosen_result["model_name"],
            "r2_score": chosen_result["r2_score"],
            "mae": chosen_result["mae"],
            "horizon_years": horizon_years,
            "projected_cagr_pct": cagr_proj,
        },
        "planning_insights": {
            "demand_outlook": "Surging" if cagr_proj > 5.0 else "Stable" if cagr_proj >= 0 else "Moderate",
            "recommendation": recommendation,
        },
        "projections": projections,
        "historical_series": [
            {
                "year": int(y),
                "applicants": int(a),
                "intake": int(i),
                "closing_rank": int(cr),
                "acceptance_rate_pct": round((i / a) * 100, 4),
            }
            for y, a, i, cr in zip(years, applicants, intake, closing_ranks)
        ],
    }
