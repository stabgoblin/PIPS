"""Exact p-median solver using network distances and capacity weights."""
from itertools import combinations
from math import comb
from fastapi import APIRouter, HTTPException
from .. import services
from ..config import DISTANCES_FILE
from ..schemas import PMedianRequest
from ..utils import load_json, ok, pending

router = APIRouter(prefix="/api/optimization", tags=["Facility Location Optimization"])

@router.get("/candidates")
def candidate_sites():
    return ok("Candidate parcels", {"candidates": services.candidates()})

@router.post("/pmedian")
def run_pmedian(request: PMedianRequest):
    sites = services.candidates()
    if request.candidate_ids is not None:
        unknown = set(request.candidate_ids) - {site["id"] for site in sites}
        if unknown:
            raise HTTPException(422, f"Unknown candidate IDs: {', '.join(sorted(unknown))}")
        sites = [site for site in sites if site["id"] in request.candidate_ids]
    if request.respect_zoning:
        zones = {"hostel_boys": {"residential_boys", "general", "undeveloped"},
                 "hostel_girls": {"residential_girls", "general", "undeveloped"}}
        allowed = zones.get(request.facility_type, {"academic", "dining", "recreation", "general", "undeveloped"})
        sites = [site for site in sites if site.get("zone") in allowed]
    if len(sites) < request.p:
        raise HTTPException(422, "Not enough eligible parcels for the requested facility count")
    matrix = load_json(DISTANCES_FILE)
    if matrix is None:
        return pending("Build the campus walking network before optimizing.", {"selected": []})
    demand = [row for row in services.facilities() if row["capacity"] > 0]
    if not demand:
        raise HTTPException(422, "No positive-capacity demand buildings available")
    pairs = {(i, j): matrix.get(row["name"], {}).get(site["id"])
             for i, row in enumerate(demand) for j, site in enumerate(sites)}
    pairs = {key: value for key, value in pairs.items() if value is not None}
    disconnected = [row["name"] for i, row in enumerate(demand)
                    if not any(a == i for a, _ in pairs)]
    if disconnected:
        raise HTTPException(422, "No eligible parcel reachable from: " + ", ".join(disconnected))
    # Exact enumeration is sufficient for a basic campus inventory and needs no
    # separately installed solver executable. Bound work before starting it.
    if comb(len(sites), request.p) * len(demand) * request.p > 2_000_000:
        raise HTTPException(422, "Too many combinations for the basic optimizer; narrow the candidate list")
    best = None
    best_cost = float("inf")
    for selection in combinations(range(len(sites)), request.p):
        assignments = []
        for i, row in enumerate(demand):
            reachable = [(pairs[i, j], j) for j in selection if (i, j) in pairs]
            if not reachable:
                break
            distance, j = min(reachable)
            assignments.append({"building": row["name"], "site": sites[j]["id"],
                                "distance_m": distance, "weight": row["capacity"]})
        if len(assignments) != len(demand):
            continue
        cost = sum(row["distance_m"] * row["weight"] for row in assignments)
        if cost < best_cost:
            best_cost = cost
            best = (selection, assignments)
    if best is None:
        raise HTTPException(422, "No feasible selection covers all demand buildings; increase the facility count")
    selection, assignments = best
    total = sum(row["distance_m"] * row["weight"] for row in assignments)
    result = {"selected": [sites[j] for j in selection],
              "assignments": assignments, "weighted_distance_m": round(total, 2),
              "average_distance_m": round(total / sum(row["capacity"] for row in demand), 2),
              "assumptions": "Capacity weights; basic zone eligibility; exported network distances.",
              "request": request.model_dump()}
    services.save_json(services.RESULTS_FILE, result)
    return ok("Optimal sites calculated", result)

@router.get("/results")
def optimization_results():
    result = load_json(services.RESULTS_FILE)
    return ok("Latest saved optimization", {"results": [result] if result else []})
