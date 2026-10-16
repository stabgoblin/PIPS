# PIPS — Predictive Infrastructure Planning

A local FastAPI backend and Streamlit dashboard for campus planning.

## Run

From the project root, install `requirements.txt` into a Python virtual environment, then run these commands in separate terminals:

```powershell
.venv\Scripts\python.exe -m uvicorn src.api.main:app --reload
.venv\Scripts\python.exe -m streamlit run src/dashboard/app.py
```

Dashboard: http://localhost:8501. API documentation: http://localhost:8000/docs.
Set `PIPS_API_URL` to use a different backend.

## Basic modules

- **Mapping:** GeoJSON building footprints, walkways, parcel inventory and graph nodes.
- **Forecasting:** regression or Holt trend smoothing, compounded annual scenarios, approximate residual-based ranges. Auto selection uses historical fit, not out-of-sample accuracy. `arima` remains a legacy alias for Holt; no ARIMA model is fitted.
- **Capacity:** inventory, utilization and threshold alerts. Add a numeric `occupancy` property to building features; missing occupancy or zero capacity yields unknown utilization. Thresholds persist in `output/thresholds.json`.
- **Accessibility:** exported shortest-path distances, disconnected pairs and building-level walking budgets at a configurable speed. These are not step-free accessibility assessments or geographic isochrone polygons.
- **Siting:** exact small-instance p-median search, using facility capacity as demand weight. All demand buildings must be reachable. Basic zone filters allow undeveloped/general parcels, enforce matching residential zones for hostels, and exclude residential zones for other types. This does not model full planning regulations or utility constraints. Large searches are rejected; the latest successful result persists in `output/optimization_results.json`.

## Data and network

The included GIS layers and generated entrance history are demonstration data, not verified NIT Trichy planning records. Applicant counts do not equal enrollment; seat suggestions are heuristics.

Replace `data/gis/sample_buildings.geojson` and `sample_paths.geojson` with `buildings.geojson` and `paths.geojson`, or edit the sample layers. Restart the API after changing which files are present. Rebuild the network after GIS changes:

```powershell
.venv\Scripts\python.exe src/gis/build_campus_graph.py
.venv\Scripts\python.exe src/gis/visualize_campus.py
```

Paths share nodes at identical digitized vertices. Crossings need explicit shared vertices; grade-separated crossings need separate modeling. Building access uses the existing 50-metre endpoint proximity rule. The sample mess, sports complex and open plot are disconnected; the optimizer correctly reports unavailable routes until genuine walkways are digitized.

Local JSON settings are intended for a single API worker. Use a transactional datastore for multi-worker deployment.

## Verify

```powershell
.venv\Scripts\python.exe -m unittest discover -s tests -v
.venv\Scripts\python.exe -m compileall -q src
```
