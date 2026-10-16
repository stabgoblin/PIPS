"""Request/response models shared by the API routers."""

from typing import Any, List, Literal, Optional

from pydantic import BaseModel, Field


class ApiResponse(BaseModel):
    status: str
    message: str
    data: Optional[Any] = None


class ForecastRequest(BaseModel):
    course_id: str = Field(..., description="Course or programme identifier")
    horizon_years: int = Field(3, ge=1, le=10)
    start_year: Optional[int] = None
    model_type: Literal["auto", "regression", "regression_linear", "regression_poly", "holt", "arima"] = "auto"
    growth_multiplier: Optional[float] = Field(1.0, ge=0.5, le=2.0, description="What-if scenario multiplier")
    notes: Optional[str] = None


class ThresholdConfig(BaseModel):
    facility_type: Optional[str] = Field(
        None, description="Facility type to apply the rule to, e.g. hostel_boys"
    )
    threshold: float = Field(
        0.85, ge=0.0, le=1.0, description="Utilization alert threshold"
    )


class PMedianRequest(BaseModel):
    p: int = Field(1, ge=1, description="Number of facilities to site")
    facility_type: Optional[str] = None
    respect_zoning: bool = True
    candidate_ids: Optional[List[str]] = None
