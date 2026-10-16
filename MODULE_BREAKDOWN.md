# Project Module Breakdown — Predictive Campus Planning

## Module 1: GIS & Campus Network Base Layer
- Digitize building footprints (hostels, classrooms, admin, sports) in QGIS
- Build walkable road network graph (nodes = intersections/buildings, edges = walkable paths)
- Map candidate undeveloped parcels and zoning constraints
- **Tools:** QGIS, GeoJSON/Shapefiles, NetworkX (for graph)
- **Output:** Campus graph + parcel inventory

## Module 2: Demand Forecasting Engine
- Ingest historical entrance exam data (registrations, appeared, passed, cutoffs, seat intake)
- Build regression / ARIMA models to predict seat demand per course (1-4 year horizon)
- **Tools:** Python (pandas, scikit-learn, statsmodels), CSV data
- **Output:** Multi-year seat demand forecast per course

## Module 3: Capacity Monitoring & Threshold Alerts
- Map physical capacity for each facility type (classroom seats, hostel beds, lab seats, mess dining spots, sports facilities)
- Calculate utilization ratio = (current students / total capacity)
- Trigger configurable alerts when threshold (e.g. 85%) is breached
- **Tools:** Python, Flask backend
- **Output:** Alert dashboard / notification system for capacity breaches

## Module 4: Facility Siting Optimizer (p-Median)
- Formulate weighted p-median problem: minimize total walking distance from demand nodes (hostels, departments) to candidate facility locations
- Respect zoning constraints (e.g. boys/girls hostel segregation, utility proximity)
- Integrate Dijkstra shortest paths from the walkable graph
- **Tools:** PuLP (LP solver), NetworkX (graph + shortest paths)
- **Output:** Ranked list of optimal parcels for new facilities with distance scores

## Module 5: Web Dashboard (Frontend)
- Interactive campus map with Leaflet.js / Mapbox
- Color-coded building occupancy heatmaps
- Siting recommendation overlays (highlighted parcels, walk paths, urgency scores)
- **Tools:** Leaflet.js, Mapbox, HTML/CSS/JS
- **Output:** Visual decision-support interface

## Module 6: Backend & Data Pipeline (Flask)
- REST API connecting GIS data, forecast engine, threshold monitor, and optimizer to frontend
- Data ingestion pipeline for entrance exam files
- Update mechanism: when construction is approved, refresh the GIS graph
- **Tools:** Flask, Python, SQLite/PostgreSQL
- **Output:** Integrated backend serving all modules

---

## Suggested Order to Build
```
Module 1 (GIS Base) → Module 2 (Forecasting) → Module 3 (Thresholds)
        ↓
Module 4 (Optimizer) → Module 6 (Backend) → Module 5 (Dashboard)
```

## Key Libraries (all Python)
| Library | Purpose |
|---------|---------|
| networkx | Graph representation, Dijkstra paths |
| pulp | p-Median LP solver |
| pandas | Data wrangling |
| scikit-learn | Regression models |
| statsmodels | ARIMA forecasting |
| flask | Backend API |
| folium/leaflet | Map visualization |
| qgis | GIS digitization |
