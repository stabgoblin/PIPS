"""Facility inventory, measured utilization, and persistent thresholds."""
from fastapi import APIRouter
from .. import services
from ..schemas import ThresholdConfig
from ..utils import ok

router = APIRouter(prefix="/api/capacity", tags=["Capacity & Threshold Monitoring"])

@router.get("/facilities")
def list_facilities():
    return ok("Facility inventory loaded", {"facilities": services.facilities()})

@router.get("/utilization")
def utilization():
    return ok("Missing occupancy is reported as unknown", {"utilization": services.facilities()})

@router.get("/alerts")
def alerts():
    rows = services.facilities()
    return ok("Capacity alerts checked", {
        "alerts": [row for row in rows if row["status"] == "alert"],
        "unknown_count": sum(row["status"] == "unknown" for row in rows),
    })

@router.get("/thresholds")
def get_thresholds():
    return ok("Active utilization thresholds", services.thresholds())

@router.post("/thresholds")
def set_thresholds(config: ThresholdConfig):
    with services.STATE_LOCK:
        rules = services.thresholds()
        if config.facility_type:
            rules["overrides"][config.facility_type] = config.threshold
        else:
            rules["default_threshold"] = config.threshold
        services.save_json(services.THRESHOLDS_FILE, rules)
    return ok("Threshold saved", rules)
