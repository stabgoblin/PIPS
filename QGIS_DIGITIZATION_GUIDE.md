# QGIS Digitization Guide — Phase 1 Step-by-Step

## Prerequisites
- Install QGIS from https://qgis.org
- Have a satellite image of your campus (Google Earth export, Google Maps screenshot, or any aerial photo)

---

## Step 1: Create QGIS Project
1. Open QGIS Desktop
2. `Project > New` → save as `campus.qgz` inside `C:\Users\amrit\Desktop\PIPS\data\gis\`

---

## Step 2: Import Base Map
**Option A — Google Satellite as basemap:**
1. `Layer > Add Layer > Add XYZ Layer`
2. Use URL: `http://mt0.google.com/vt/lyrs=s&hl=en&x={x}&y={y}&z={z}` (Google Satellite)

**Option B — Import image:**
1. `Layer > Add Layer > Add Raster Layer`
2. Select your campus image file
3. If the image has no georeference, you'll need to georeference it: `Raster > Georeferencer`

---

## Step 3: Create Buildings Layer
1. `Layer > Create Layer > New Shapefile Layer`
2. Settings:
   - File name: `buildings`
   - Geometry type: **Polygon**
3. Add fields (columns):
   | Field Name | Type | Length |
   |-----------|------|--------|
   | name | Text | 100 |
   | type | Text | 50 |
   | zone | Text | 50 |
   | capacity | Whole number | 10 |
   | floors | Whole number | 5 |
   | notes | Text | 200 |
4. Click OK

### Building Types (use in `type` field):
```
academic          — classrooms, labs, departments
hostel_boys       — boys hostels
hostel_girls      — girls hostels
mess              — dining halls
admin             — admin block, offices
sports            — gym, sports complex, fields
library           — library building
parking           — parking areas
open_land         — undeveloped plots
candidate_site    — potential construction sites
```

### Digitize Each Building:
1. Select the buildings layer → Toggle Editing (pencil icon)
2. Click `Add Polygon Feature` button
3. Click corners of the building on the map to draw its outline
4. Right-click to finish the polygon
5. Fill in the attribute fields (name, type, zone, capacity, floors)
6. Save edits (floppy disk icon)

---

## Step 4: Create Paths Layer
1. `Layer > Create Layer > New Shapefile Layer`
2. Settings:
   - File name: `paths`
   - Geometry type: **LineString**
3. Add fields:
   | Field Name | Type | Length |
   |-----------|------|--------|
   | name | Text | 100 |
   | type | Text | 50 |
   | surface | Text | 30 |
   | width_meters | Decimal number | 5 |
   | notes | Text | 200 |
4. Click OK

### Path Types (use in `type` field):
```
road              — vehicle roads
walkway           — pedestrian paths
shortcut          — dirt/shortcut paths
```

### Digitize Each Path:
1. Toggle Editing on paths layer
2. Click `Add Line Feature`
3. Click along the path — place points at every **turn or intersection**
4. Right-click to finish
5. Fill in name, type, surface
6. Save edits

---

## Step 5: Export as GeoJSON
For each layer:
1. Right-click layer → `Export > Save Features As...`
2. Format: **GeoJSON**
3. Save to: `C:\Users\amrit\Desktop\PIPS\data\gis\`
4. File names: `buildings.geojson`, `paths.geojson`

---

## Step 6: Run the Graph Builder
Open terminal and run:
```bash
cd C:\Users\amrit\Desktop\PIPS
python src/gis/build_campus_graph.py
```

---

## Tips
- **Accuracy matters** — Use satellite imagery as background for precise placement
- **Name everything** — Use descriptive names (e.g., "CSE Block", "Boys Hostel 3")
- **Mark open plots** — Even empty land matters for the optimizer (candidate sites)
- **Intersections** — Place path nodes at every junction where paths cross
- **Scale** — Your campus is 200+ acres; expect 15-30 buildings and 20-40 paths

---

## What Your Mentor Wants to See Tomorrow
- QGIS installed and open
- Satellite base map loaded
- First 2-3 buildings digitized (even rough outlines)
- Understanding of the 6 modules (see MODULE_BREAKDOWN.md)
