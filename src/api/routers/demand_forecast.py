"""Student demand forecasting endpoints.

Module 2 - demand forecasting engine. Connected to pandas / scikit-learn /
statsmodels pipeline in src/forecast/engine.py.
"""

from fastapi import APIRouter, HTTPException

from ..config import EXAM_DIR, EXAM_FILE
from ..schemas import ForecastRequest
from ..utils import error, ok, pending
from ...forecast import engine

router = APIRouter(prefix="/api/forecast", tags=["Student Demand Forecasting"])


@router.get("/courses")
def list_courses():
    """List available engineering courses with current metrics."""
    try:
        courses = engine.get_available_courses()
        return ok(f"{len(courses)} courses loaded", {"courses": courses})
    except Exception as exc:
        return error(f"Failed to load course list: {exc}", {"courses": []})


@router.get("/overview")
def department_overview():
    """Cross-department summary of applicant numbers, preference share, and intake."""
    try:
        summary = engine.get_all_courses_summary()
        return ok("Institution demand overview loaded", summary)
    except Exception as exc:
        return error(f"Failed to load demand overview: {exc}")


@router.get("/history/{course_id}")
def course_history(course_id: str):
    """Retrieve full historical time-series for a specific course."""
    records = engine.get_course_history(course_id)
    if records is None:
        raise HTTPException(status_code=404, detail=f"Course '{course_id}' not found.")
    return ok(f"Historical demand for '{course_id.upper()}' loaded", {
        "course_id": course_id.upper(),
        "count": len(records),
        "history": records,
    })


@router.post("/predict")
def predict_demand(request: ForecastRequest):
    """Run regression and ARIMA forecasting for course seat demand."""
    try:
        if request.start_year is not None:
            raise HTTPException(422, "Forecasts start after the latest observation; omit start_year.")
        result = engine.predict_demand(
            course_id=request.course_id,
            horizon_years=request.horizon_years,
            model_type=request.model_type or "auto",
            growth_multiplier=request.growth_multiplier or 1.0,
        )
        return ok(f"Demand forecast generated for {request.course_id.upper()}", result)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc))
    except HTTPException:
        raise
    except Exception as exc:
        return error(f"Forecasting error: {exc}")


@router.get("/datasets")
def list_datasets():
    """List ingested entrance exam datasets."""
    files = []
    if EXAM_DIR.exists():
        for path in EXAM_DIR.glob("*.csv"):
            try:
                with open(path, "r", encoding="utf-8") as handle:
                    line_count = sum(1 for _ in handle) - 1
            except Exception:
                line_count = 0
            files.append({
                "filename": path.name,
                "path": str(path),
                "size_bytes": path.stat().st_size,
                "records": max(0, line_count),
                "active": path.resolve() == EXAM_FILE.resolve(),
            })

    return ok(f"{len(files)} exam dataset(s) found", {"datasets": files})
