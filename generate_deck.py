import sys
from pathlib import Path
import pptx
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

def create_deck(output_path: str):
    prs = pptx.Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Color Palette Definitions
    BG_DARK = RGBColor(15, 23, 42)        # Slate 900
    BG_LIGHT = RGBColor(248, 250, 252)    # Slate 50
    CARD_BG = RGBColor(255, 255, 255)     # White
    CARD_BORDER = RGBColor(226, 232, 240)# Slate 200
    
    PRIMARY = RGBColor(37, 99, 235)       # Royal Blue (Tailwind Blue 600)
    PRIMARY_DARK = RGBColor(29, 78, 216)  # Dark Blue
    PRIMARY_LIGHT = RGBColor(239, 246, 255) # Light Blue 50
    
    TEXT_DARK = RGBColor(15, 23, 42)      # Slate 900
    TEXT_MUTED = RGBColor(100, 116, 139)  # Slate 500
    TEXT_LIGHT = RGBColor(255, 255, 255)  # White
    
    SUCCESS = RGBColor(16, 185, 129)      # Emerald 500
    SUCCESS_LIGHT = RGBColor(236, 253, 245)
    SUCCESS_BORDER = RGBColor(167, 243, 208)
    
    WARNING = RGBColor(245, 158, 11)      # Amber 500
    WARNING_LIGHT = RGBColor(254, 243, 199)
    WARNING_BORDER = RGBColor(253, 230, 138)
    
    ACCENT_PURPLE = RGBColor(124, 58, 237) # Purple 600

    def add_header(slide, title_text, category_text, dark=False):
        # Category Chip / Subtitle
        cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(0.4))
        tf_cat = cat_box.text_frame
        tf_cat.word_wrap = True
        tf_cat.margin_left = tf_cat.margin_right = tf_cat.margin_top = tf_cat.margin_bottom = 0
        p_cat = tf_cat.paragraphs[0]
        p_cat.text = category_text.upper()
        p_cat.font.size = Pt(11)
        p_cat.font.bold = True
        p_cat.font.color.rgb = PRIMARY if dark else PRIMARY
        
        # Title
        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.75), Inches(11.7), Inches(0.8))
        tf = title_box.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        p.text = title_text
        p.font.size = Pt(24)
        p.font.bold = True
        p.font.color.rgb = TEXT_LIGHT if dark else TEXT_DARK

    def set_slide_bg(slide, color):
        bg = slide.background
        fill = bg.fill
        fill.solid()
        fill.fore_color.rgb = color

    def add_card(slide, left, top, width, height, bg_color=CARD_BG, border_color=CARD_BORDER):
        shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        shape.fill.solid()
        shape.fill.fore_color.rgb = bg_color
        shape.line.color.rgb = border_color
        shape.line.width = Pt(1)
        return shape

    # =========================================================================
    # SLIDE 1: Title Slide (Dark Theme)
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s1, BG_DARK)
    
    # Hero Title Box
    tbox = s1.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(11.3), Inches(3.8))
    tf1 = tbox.text_frame
    tf1.word_wrap = True
    
    p = tf1.paragraphs[0]
    p.text = "PIPS: Predictive Infrastructure Planning System"
    p.font.size = Pt(36)
    p.font.bold = True
    p.font.color.rgb = TEXT_LIGHT
    p.space_after = Pt(14)
    
    p2 = tf1.add_paragraph()
    p2.text = "A GeoAI & Network Optimization System for Proactive Campus Infrastructure Planning"
    p2.font.size = Pt(18)
    p2.font.color.rgb = RGBColor(147, 197, 253) # Light Blue 300
    p2.space_after = Pt(28)
    
    p3 = tf1.add_paragraph()
    p3.text = "PROJECT STATUS REVIEW & ARCHITECTURE PRESENTATION"
    p3.font.size = Pt(13)
    p3.font.bold = True
    p3.font.color.rgb = RGBColor(226, 232, 240)
    p3.space_after = Pt(10)
    
    p4 = tf1.add_paragraph()
    p4.text = "Covers: Project Summary | 6 Modules & Working Principles | Work Done Till Now | Work Pending"
    p4.font.size = Pt(13)
    p4.font.color.rgb = TEXT_MUTED

    # Bottom Pill
    badge = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), Inches(5.8), Inches(11.33), Inches(0.7))
    badge.fill.solid()
    badge.fill.fore_color.rgb = RGBColor(30, 41, 59)
    badge.line.color.rgb = RGBColor(51, 65, 85)
    btf = badge.text_frame
    btf.vertical_anchor = MSO_ANCHOR.MIDDLE
    bp = btf.paragraphs[0]
    bp.text = "Key Technologies: GIS & GeoPandas | NetworkX Graph Analytics | Scikit-Learn & Statsmodels | PuLP ILP Siter | FastAPI | Streamlit"
    bp.font.size = Pt(12)
    bp.font.color.rgb = RGBColor(203, 213, 225)
    bp.alignment = PP_ALIGN.CENTER

    # =========================================================================
    # SLIDE 2: Project Summary & Motivation
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s2, BG_LIGHT)
    add_header(s2, "Project Executive Summary & Motivation", "Introduction & Context")

    # Left Card: The Problem
    add_card(s2, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.3))
    t1 = s2.shapes.add_textbox(Inches(1.1), Inches(1.8), Inches(5.0), Inches(4.8))
    tf = t1.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "Current Bottleneck: Reactive Planning"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = RGBColor(220, 38, 38) # Red
    p.space_after = Pt(14)

    points_left = [
        ("Lagging Decisions: ", "New hostels and lecture halls are commissioned only AFTER overcrowding, bed deficits, and classroom congestion have already occurred."),
        ("Intuitive / Political Siting: ", "Site selection for new construction is manual and political, ignoring pedestrian walking times, topological networks, and zoning constraints."),
        ("Unused Predictive Signals: ", "Rich entrance exam indicators (JEE/JoSAA applicant counts, cutoffs, pass rates) are archived as static records rather than leveraged for multi-year enrollment projections."),
        ("Campus Scale Complexity: ", "On large campuses (200+ acres), placing facilities poorly causes cumulative commute fatigue for thousands of students daily.")
    ]
    for b_title, b_desc in points_left:
        p = tf.add_paragraph()
        p.space_after = Pt(10)
        run1 = p.add_run()
        run1.text = "• " + b_title
        run1.font.bold = True
        run1.font.size = Pt(12)
        run1.font.color.rgb = TEXT_DARK
        run2 = p.add_run()
        run2.text = b_desc
        run2.font.size = Pt(12)
        run2.font.color.rgb = TEXT_MUTED

    # Right Card: The PIPS Solution
    add_card(s2, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.3))
    t2 = s2.shapes.add_textbox(Inches(7.1), Inches(1.8), Inches(5.1), Inches(4.8))
    tf2 = t2.text_frame
    tf2.word_wrap = True
    p = tf2.paragraphs[0]
    p.text = "The PIPS Solution: Proactive & Scientific"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = PRIMARY
    p.space_after = Pt(14)

    points_right = [
        ("Multi-Year Predictive Forecasting: ", "Translates national entrance examination trends into 1-to-5-year seat demand trajectories per academic department."),
        ("Threshold-Driven Capacity Alerts: ", "Continuously tracks utilization ratios (students/bed, students/seat) and triggers warnings BEFORE 85% safety limits are breached."),
        ("Mathematical Siting (p-Median): ", "Formulates facility location as an Integer Linear Program (ILP) on a digitized walkability graph to minimize aggregate student walking distance."),
        ("Interactive Decision Dashboard: ", "Provides campus planners with an interactive GIS map, scenario simulation sliders, and visual decision-support reports.")
    ]
    for b_title, b_desc in points_right:
        p = tf2.add_paragraph()
        p.space_after = Pt(10)
        run1 = p.add_run()
        run1.text = "• " + b_title
        run1.font.bold = True
        run1.font.size = Pt(12)
        run1.font.color.rgb = TEXT_DARK
        run2 = p.add_run()
        run2.text = b_desc
        run2.font.size = Pt(12)
        run2.font.color.rgb = TEXT_MUTED

    # =========================================================================
    # SLIDE 3: System Architecture & Main Working Principle
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s3, BG_LIGHT)
    add_header(s3, "System Architecture & End-to-End Working Principle", "System Workflow")

    # 3 Workflow Columns
    cols_data = [
        ("1. Data & Spatial Layer", PRIMARY, [
            ("Entrance Exam History", "10-year CSV data: applicants, ranks, cutoffs, seat intake."),
            ("Campus GIS Digitization", "QGIS footprints for buildings, candidate parcels, and walkable paths."),
            ("GeoJSON Conversion", "Standardized coordinate layers with building attributes & capacities.")
        ]),
        ("2. Analytics & Solvers", ACCENT_PURPLE, [
            ("Demand Engine (Module 2)", "Polynomial Ridge & Holt-Winters forecasting with auto model selection."),
            ("Capacity Monitor (Module 3)", "Utilization ratios & configurable threshold breach detection."),
            ("Network Graph & Shortest Paths", "NetworkX Dijkstra walking distance matrix on pedestrian graph."),
            ("p-Median Optimizer (Module 5)", "PuLP ILP solver finding optimal sites minimizing walking distance.")
        ]),
        ("3. Decision Support Interface", SUCCESS, [
            ("FastAPI Backend (Module 6)", "High-performance REST API routing requests across all modules."),
            ("Interactive Streamlit UI", "Folium Leaflet campus maps, scenario sliders & metric dashboards."),
            ("Closed-Loop Feedback", "Approved constructions update the GIS network graph dynamically.")
        ])
    ]

    for i, (title, color, items) in enumerate(cols_data):
        cx = Inches(0.8 + i * 3.95)
        add_card(s3, cx, Inches(1.6), Inches(3.75), Inches(5.3))
        tb = s3.shapes.add_textbox(cx + Inches(0.25), Inches(1.85), Inches(3.25), Inches(4.8))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(16)
        p.font.bold = True
        p.font.color.rgb = color
        p.space_after = Pt(14)

        for heading, desc in items:
            p = tf.add_paragraph()
            p.space_after = Pt(10)
            r1 = p.add_run()
            r1.text = "• " + heading + "\n  "
            r1.font.bold = True
            r1.font.size = Pt(12)
            r1.font.color.rgb = TEXT_DARK
            r2 = p.add_run()
            r2.text = desc
            r2.font.size = Pt(11)
            r2.font.color.rgb = TEXT_MUTED

    # =========================================================================
    # SLIDE 4: Module 1 — GIS & Campus Network Base Layer
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s4, BG_LIGHT)
    add_header(s4, "Module 1: GIS & Campus Network Base Layer", "Campus Spatial Digital Twin")

    add_card(s4, Inches(0.8), Inches(1.6), Inches(6.8), Inches(5.3))
    tb = s4.shapes.add_textbox(Inches(1.1), Inches(1.8), Inches(6.2), Inches(4.8))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "Core Working Principle"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = PRIMARY
    p.space_after = Pt(12)

    m1_points = [
        ("Spatial Digitization in QGIS: ", "Satellite imagery is used as a basemap to digitize building polygons (academic blocks, hostels, mess, sports), open parcels, and line-string walkable paths."),
        ("Graph Topology Construction: ", "The vector geometry is ingested via GeoPandas and converted into a NetworkX mathematical graph. Building centroids and path intersections become graph nodes; walkways become graph edges."),
        ("Metric Edge Weighting: ", "Haversine geodesic distance calculates the precise physical walking distance in meters between every pair of connected nodes."),
        ("Access Edge Binding: ", "Building centroid nodes are automatically connected to nearby path intersections within a 50m threshold radius, forming an integrated walkable network.")
    ]
    for b_title, b_desc in m1_points:
        p = tf.add_paragraph()
        p.space_after = Pt(10)
        r1 = p.add_run()
        r1.text = "• " + b_title
        r1.font.bold = True
        r1.font.size = Pt(12)
        r1.font.color.rgb = TEXT_DARK
        r2 = p.add_run()
        r2.text = b_desc
        r2.font.size = Pt(11)
        r2.font.color.rgb = TEXT_MUTED

    # Right Card: Outputs & Artifacts
    add_card(s4, Inches(7.9), Inches(1.6), Inches(4.6), Inches(5.3))
    tb_r = s4.shapes.add_textbox(Inches(8.15), Inches(1.8), Inches(4.1), Inches(4.8))
    tf_r = tb_r.text_frame
    tf_r.word_wrap = True
    p = tf_r.paragraphs[0]
    p.text = "Module Artifacts & Outputs"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = TEXT_DARK
    p.space_after = Pt(14)

    m1_outputs = [
        ("campus_graph.graphml: ", "Persisted NetworkX graph containing nodes, attributes, and weighted walk edges."),
        ("building_distances.json: ", "Precomputed walking distance matrix between all campus facilities."),
        ("campus_map.html: ", "Interactive Leaflet/Folium map rendering building polygons, zones, and walkways."),
        ("Standard GeoJSON Layers: ", "Clean GeoJSON schemas for buildings and pathways matching QGIS standards.")
    ]
    for h, d in m1_outputs:
        p = tf_r.add_paragraph()
        p.space_after = Pt(12)
        r1 = p.add_run()
        r1.text = "✔ " + h
        r1.font.bold = True
        r1.font.size = Pt(12)
        r1.font.color.rgb = SUCCESS
        r2 = p.add_run()
        r2.text = d
        r2.font.size = Pt(11)
        r2.font.color.rgb = TEXT_MUTED

    # =========================================================================
    # SLIDE 5: Module 2 — Student Demand Forecasting Engine
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s5, BG_LIGHT)
    add_header(s5, "Module 2: Student Demand Forecasting Engine", "Predictive Analytics")

    add_card(s5, Inches(0.8), Inches(1.6), Inches(6.8), Inches(5.3))
    tb = s5.shapes.add_textbox(Inches(1.1), Inches(1.8), Inches(6.2), Inches(4.8))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "Core Working Principle"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = PRIMARY
    p.space_after = Pt(12)

    m2_points = [
        ("Multi-Metric Ingestion: ", "Ingests 10-year historical time series of national entrance exams (JEE/JoSAA): registered candidates, appeared, qualifying cutoffs, opening/closing ranks, and sanctioned seats per branch."),
        ("Dual-Model Predictive Pipeline: ", "Simultaneously trains two distinct algorithms: (1) Polynomial Ridge Regression (scikit-learn) with L2 regularization to capture non-linear curvature, and (2) Holt-Winters Exponential Smoothing (statsmodels) for trend extrapolation."),
        ("Automated Model Selection: ", "Automatically selects the winning model per course based on statistical goodness-of-fit: maximizing Coefficient of Determination (R²) and minimizing Mean Absolute Error (MAE)."),
        ("What-If Scenario Simulation: ", "Supports customizable growth multipliers (0.8x to 1.5x) to test policy interventions, new degree launches, or quota expansions.")
    ]
    for b_title, b_desc in m2_points:
        p = tf.add_paragraph()
        p.space_after = Pt(10)
        r1 = p.add_run()
        r1.text = "• " + b_title
        r1.font.bold = True
        r1.font.size = Pt(12)
        r1.font.color.rgb = TEXT_DARK
        r2 = p.add_run()
        r2.text = b_desc
        r2.font.size = Pt(11)
        r2.font.color.rgb = TEXT_MUTED

    # Right Card: Forecasting Metrics
    add_card(s5, Inches(7.9), Inches(1.6), Inches(4.6), Inches(5.3))
    tb_r = s5.shapes.add_textbox(Inches(8.15), Inches(1.8), Inches(4.1), Inches(4.8))
    tf_r = tb_r.text_frame
    tf_r.word_wrap = True
    p = tf_r.paragraphs[0]
    p.text = "Forecasting Outputs & Indicators"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = TEXT_DARK
    p.space_after = Pt(14)

    m2_outputs = [
        ("1 to 5-Year Horizon Demand: ", "Course-wise projected applicant volume and seat demand."),
        ("Selectivity Trajectory: ", "Tracks closing ranks and applicants-per-seat ratios over time."),
        ("Infrastructure Urgency Score: ", "Translates high demand growth into concrete seat deficit estimates for planning."),
        ("Evaluation Accuracy: ", "Reports R² score and MAE for transparent model explainability.")
    ]
    for h, d in m2_outputs:
        p = tf_r.add_paragraph()
        p.space_after = Pt(12)
        r1 = p.add_run()
        r1.text = "✔ " + h
        r1.font.bold = True
        r1.font.size = Pt(12)
        r1.font.color.rgb = PRIMARY
        r2 = p.add_run()
        r2.text = d
        r2.font.size = Pt(11)
        r2.font.color.rgb = TEXT_MUTED

    # =========================================================================
    # SLIDE 6: Module 3 & Module 4 — Capacity & Accessibility
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s6, BG_LIGHT)
    add_header(s6, "Modules 3 & 4: Capacity Monitoring & Accessibility", "Operational Intelligence")

    # Left Card: Module 3
    add_card(s6, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.3))
    tb_m3 = s6.shapes.add_textbox(Inches(1.1), Inches(1.8), Inches(5.0), Inches(4.8))
    tf = tb_m3.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "Module 3: Capacity & Threshold Monitoring"
    p.font.size = Pt(17)
    p.font.bold = True
    p.font.color.rgb = PRIMARY
    p.space_after = Pt(12)

    m3_items = [
        ("Physical Capacity Mapping: ", "Catalogs true maximum capacity per facility: classroom lecture seats, hostel beds, lab benches, and mess dining capacities."),
        ("Utilization Ratio: ", "Computes Utilization = (Current/Projected Students) / Design Capacity across every building type."),
        ("Configurable Safety Margins: ", "User-adjustable alert thresholds (e.g., 85% safety buffer)."),
        ("Multi-Tier Alerts: ", "Flags facilities into Normal (<85%), Warning (85-95%), and Critical Breach (>95%) to trigger immediate capital expansion reviews.")
    ]
    for h, d in m3_items:
        p = tf.add_paragraph()
        p.space_after = Pt(8)
        r1 = p.add_run()
        r1.text = "• " + h
        r1.font.bold = True
        r1.font.size = Pt(11)
        r1.font.color.rgb = TEXT_DARK
        r2 = p.add_run()
        r2.text = d
        r2.font.size = Pt(11)
        r2.font.color.rgb = TEXT_MUTED

    # Right Card: Module 4
    add_card(s6, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.3))
    tb_m4 = s6.shapes.add_textbox(Inches(7.1), Inches(1.8), Inches(5.1), Inches(4.8))
    tf = tb_m4.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "Module 4: Campus Accessibility & Reachability"
    p.font.size = Pt(17)
    p.font.bold = True
    p.font.color.rgb = ACCENT_PURPLE
    p.space_after = Pt(12)

    m4_items = [
        ("Dijkstra Shortest Path Search: ", "Executes all-pairs shortest path analysis across the NetworkX walkable graph to calculate realistic walking commutes."),
        ("N×N Distance Matrix: ", "Provides an instant distance lookup (in meters) between any origin and destination facility."),
        ("Isolated Gap Analysis: ", "Identifies disconnected or inaccessible structures where pedestrian walkways are broken or missing."),
        ("Walking Isochrones (Service Areas): ", "Models 5-minute and 10-minute pedestrian catchment zones around major amenities (mess, library, health center).")
    ]
    for h, d in m4_items:
        p = tf.add_paragraph()
        p.space_after = Pt(8)
        r1 = p.add_run()
        r1.text = "• " + h
        r1.font.bold = True
        r1.font.size = Pt(11)
        r1.font.color.rgb = TEXT_DARK
        r2 = p.add_run()
        r2.text = d
        r2.font.size = Pt(11)
        r2.font.color.rgb = TEXT_MUTED

    # =========================================================================
    # SLIDE 7: Module 5 — Facility Location Optimizer (p-Median)
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s7, BG_LIGHT)
    add_header(s7, "Module 5: Facility Location Optimizer (p-Median)", "Mathematical Optimization")

    add_card(s7, Inches(0.8), Inches(1.6), Inches(6.8), Inches(5.3))
    tb = s7.shapes.add_textbox(Inches(1.1), Inches(1.8), Inches(6.2), Inches(4.8))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "Mathematical Formulation & Working Principle"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = PRIMARY
    p.space_after = Pt(12)

    m5_points = [
        ("Integer Linear Programming (ILP): ", "Formulated as a classic p-Median facility location problem, solved using PuLP and the CBC open-source solver."),
        ("Mathematical Objective: ", "Minimize total weighted walking distance:\n    min ∑ (w_i · d_ij · x_ij)\nwhere w_i is the student population at demand node i, d_ij is the shortest walking distance to candidate parcel j, and x_ij is the binary assignment variable."),
        ("Selection Constraint: ", "Exactly p candidate parcels are selected from the pool of available undeveloped campus zones: ∑ y_j = p."),
        ("Strict Zoning Rules: ", "Integrates campus zoning constraints — ensuring residential facilities adhere to segregation rules (e.g. boys/girls zones) and maintaining utility buffer corridors.")
    ]
    for b_title, b_desc in m5_points:
        p = tf.add_paragraph()
        p.space_after = Pt(10)
        r1 = p.add_run()
        r1.text = "• " + b_title
        r1.font.bold = True
        r1.font.size = Pt(12)
        r1.font.color.rgb = TEXT_DARK
        r2 = p.add_run()
        r2.text = b_desc
        r2.font.size = Pt(11)
        r2.font.color.rgb = TEXT_MUTED

    # Right Card: Why p-Median matters
    add_card(s7, Inches(7.9), Inches(1.6), Inches(4.6), Inches(5.3))
    tb_r = s7.shapes.add_textbox(Inches(8.15), Inches(1.8), Inches(4.1), Inches(4.8))
    tf_r = tb_r.text_frame
    tf_r.word_wrap = True
    p = tf_r.paragraphs[0]
    p.text = "Strategic Advantages"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = TEXT_DARK
    p.space_after = Pt(14)

    adv_points = [
        ("Evidence-Based Construction: ", "Eliminates subjective guesswork by replacing committee opinions with mathematical proof of optimal placement."),
        ("Minimizes Student Fatigue: ", "Guarantees the lowest possible average daily walking distance between hostels, mess, and lecture complexes."),
        ("Efficient Land Utilization: ", "Ranks candidate open parcels by accessibility index, protecting campus green belts from haphazard encroachment."),
        ("Multi-Facility Siting: ", "Simultaneously determines sites for p=1, 2, or more buildings concurrently.")
    ]
    for h, d in adv_points:
        p = tf_r.add_paragraph()
        p.space_after = Pt(12)
        r1 = p.add_run()
        r1.text = "★ " + h
        r1.font.bold = True
        r1.font.size = Pt(12)
        r1.font.color.rgb = PRIMARY
        r2 = p.add_run()
        r2.text = d
        r2.font.size = Pt(11)
        r2.font.color.rgb = TEXT_MUTED

    # =========================================================================
    # SLIDE 8: Module 6 — Unified REST API & Interactive Dashboard
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s8, BG_LIGHT)
    add_header(s8, "Module 6: Unified REST API & Decision Dashboard", "Software Architecture")

    # Left Card: FastAPI Backend
    add_card(s8, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.3))
    tb_api = s8.shapes.add_textbox(Inches(1.1), Inches(1.8), Inches(5.0), Inches(4.8))
    tf = tb_api.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "FastAPI Backend Architecture"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = PRIMARY
    p.space_after = Pt(12)

    api_points = [
        ("Modular Micro-Routers: ", "Isolated endpoints for each domain:\n  - /api/mapping (footprints, paths, centroids)\n  - /api/forecast (predictions, historical series)\n  - /api/capacity (utilization, thresholds)\n  - /api/accessibility (distances, reachability)\n  - /api/optimization (p-median siting)"),
        ("Type-Safe Pydantic Schemas: ", "Strict request/response validation ensuring reliability."),
        ("CORS & OpenAPI Integration: ", "Automatic interactive Swagger UI (/docs) and seamless frontend integration.")
    ]
    for h, d in api_points:
        p = tf.add_paragraph()
        p.space_after = Pt(8)
        r1 = p.add_run()
        r1.text = "• " + h
        r1.font.bold = True
        r1.font.size = Pt(11)
        r1.font.color.rgb = TEXT_DARK
        r2 = p.add_run()
        r2.text = d
        r2.font.size = Pt(11)
        r2.font.color.rgb = TEXT_MUTED

    # Right Card: Streamlit Dashboard
    add_card(s8, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.3))
    tb_ui = s8.shapes.add_textbox(Inches(7.1), Inches(1.8), Inches(5.1), Inches(4.8))
    tf = tb_ui.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "Streamlit Decision Dashboard"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = ACCENT_PURPLE
    p.space_after = Pt(12)

    ui_points = [
        ("7 Dedicated Views: ", "Home, Campus Mapping, Student Demand Forecasting, Capacity Monitoring, Campus Accessibility, Facility Optimizer, and API Health Status."),
        ("Interactive Geospatial Maps: ", "Integrated Folium maps rendering building polygons with popup details, zoning colors, and walkable path overlays."),
        ("Dynamic Scenario Sliders: ", "Real-time horizon adjustment (1-5 years), model toggling, and what-if growth multipliers with instant re-rendering."),
        ("Visual Decision Support: ", "Clean metric scorecards, progress bars, and alert badges for administrative decision-makers.")
    ]
    for h, d in ui_points:
        p = tf.add_paragraph()
        p.space_after = Pt(8)
        r1 = p.add_run()
        r1.text = "• " + h
        r1.font.bold = True
        r1.font.size = Pt(11)
        r1.font.color.rgb = TEXT_DARK
        r2 = p.add_run()
        r2.text = d
        r2.font.size = Pt(11)
        r2.font.color.rgb = TEXT_MUTED

    # =========================================================================
    # SLIDE 9: Work Done Till Now (Current Implementation Status)
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s9, BG_LIGHT)
    add_header(s9, "Current Implementation Status: Work Done Till Now", "Project Progress")

    # 3 Category Cards
    done_categories = [
        ("GIS & Network Layer", SUCCESS, [
            ("QGIS Digitization Pipeline: ", "Standardized GeoJSON schemas established for campus structures, parcels, and pathways."),
            ("Graph Builder Engine: ", "src/gis/build_campus_graph.py successfully converts GeoJSON polygons into topological NetworkX graphs."),
            ("Distance & Map Outputs: ", "Generates campus_graph.graphml, precomputed building_distances.json, and campus_map.html.")
        ]),
        ("Demand Forecasting Engine", PRIMARY, [
            ("Historical Admission Dataset: ", "10-year realistic entrance exam dataset (entrance_exam_history.csv) across major engineering branches."),
            ("Dual ML Predictive Pipeline: ", "Fully implemented Polynomial Ridge Regression and Holt-Winters Exponential Smoothing in src/forecast/engine.py."),
            ("Automated Evaluation: ", "Automatic selection using R² & MAE, plus interactive what-if scenario multipliers.")
        ]),
        ("Full-Stack Backend & UI", ACCENT_PURPLE, [
            ("FastAPI Modular Backend: ", "FastAPI server running with structured schemas, CORS, and 5 modular router endpoints."),
            ("Streamlit Decision UI: ", "Interactive 7-page dashboard with Folium map rendering and live forecast visualization."),
            ("Live Module Integration: ", "Module 1 (GIS Mapping) and Module 2 (Forecasting) are fully wired end-to-end from API to UI.")
        ])
    ]

    for i, (cat_title, color, tasks) in enumerate(done_categories):
        cx = Inches(0.8 + i * 3.95)
        add_card(s9, cx, Inches(1.6), Inches(3.75), Inches(5.3), bg_color=CARD_BG, border_color=CARD_BORDER)
        tb = s9.shapes.add_textbox(cx + Inches(0.2), Inches(1.85), Inches(3.35), Inches(4.8))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = cat_title
        p.font.size = Pt(16)
        p.font.bold = True
        p.font.color.rgb = color
        p.space_after = Pt(14)

        for heading, desc in tasks:
            p = tf.add_paragraph()
            p.space_after = Pt(10)
            r1 = p.add_run()
            r1.text = "✔ " + heading + "\n  "
            r1.font.bold = True
            r1.font.size = Pt(11)
            r1.font.color.rgb = SUCCESS
            r2 = p.add_run()
            r2.text = desc
            r2.font.size = Pt(11)
            r2.font.color.rgb = TEXT_MUTED

    # =========================================================================
    # SLIDE 10: Work Pending (Technical Roadmap & Next Steps)
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s10, BG_LIGHT)
    add_header(s10, "Technical Roadmap: Work Pending & Next Milestones", "Future Work")

    # 3 Category Cards
    pending_categories = [
        ("Module 5: PuLP Siting Solver", WARNING, [
            ("Implement ILP Siting Model: ", "Write the complete p-median optimization formulation in src/optimizer/ using PuLP and CBC solver."),
            ("Candidate Site Integration: ", "Parse candidate open parcels from GeoJSON and compute walking distances from all campus demand nodes."),
            ("Zoning Rule Enforcement: ", "Encode hard constraints for residential gender segregation and utility proximity buffers.")
        ]),
        ("Modules 3 & 4: Capacity & Gaps", PRIMARY, [
            ("Live Capacity Monitoring: ", "Wire facility tables to live student enrollment databases and compute dynamic utilization ratios."),
            ("Automated Threshold Alerting: ", "Implement trigger thresholds (e.g. 85%) to send proactive warning notifications in the dashboard."),
            ("Isochrone Catchment Overlays: ", "Render 5 and 10-minute pedestrian walking service areas and flag unreachable campus gaps.")
        ]),
        ("GIS Scale & Closed-Loop", ACCENT_PURPLE, [
            ("Full-Scale Campus Digitization: ", "Digitize the entire 200+ acre campus footprint and actual road paths in QGIS, replacing sample files."),
            ("Automated Decision Loop: ", "Auto-feed Module 2 forecasted deficits directly into Module 3 alerts, triggering Module 5 optimal siting recommendations."),
            ("Construction Update Flow: ", "Allow approved construction sites to automatically refresh the GIS network graph.")
        ])
    ]

    for i, (cat_title, color, tasks) in enumerate(pending_categories):
        cx = Inches(0.8 + i * 3.95)
        add_card(s10, cx, Inches(1.6), Inches(3.75), Inches(5.3), bg_color=CARD_BG, border_color=CARD_BORDER)
        tb = s10.shapes.add_textbox(cx + Inches(0.2), Inches(1.85), Inches(3.35), Inches(4.8))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = cat_title
        p.font.size = Pt(16)
        p.font.bold = True
        p.font.color.rgb = color
        p.space_after = Pt(14)

        for heading, desc in tasks:
            p = tf.add_paragraph()
            p.space_after = Pt(10)
            r1 = p.add_run()
            r1.text = "⏳ " + heading + "\n  "
            r1.font.bold = True
            r1.font.size = Pt(11)
            r1.font.color.rgb = WARNING
            r2 = p.add_run()
            r2.text = desc
            r2.font.size = Pt(11)
            r2.font.color.rgb = TEXT_MUTED

    # =========================================================================
    # SLIDE 11: Module Progress Matrix (Summary Table)
    # =========================================================================
    s11 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s11, BG_LIGHT)
    add_header(s11, "Module Completion Status Matrix", "Current Milestone Audit")

    # Table
    table_shape = s11.shapes.add_table(7, 4, Inches(0.8), Inches(1.6), Inches(11.73), Inches(5.2))
    table = table_shape.table
    table.columns[0].width = Inches(3.2)
    table.columns[1].width = Inches(2.2)
    table.columns[2].width = Inches(1.8)
    table.columns[3].width = Inches(4.53)

    headers = ["Module Name", "Primary Technologies", "Status", "Current Implementation State"]
    for col_idx, h in enumerate(headers):
        cell = table.cell(0, col_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = RGBColor(30, 41, 59)
        p = cell.text_frame.paragraphs[0]
        p.text = h
        p.font.bold = True
        p.font.size = Pt(12)
        p.font.color.rgb = TEXT_LIGHT

    rows_data = [
        ("Module 1: GIS & Network Base", "QGIS, GeoPandas, NetworkX", "COMPLETE", "Graph builder, GeoJSON layers, distance matrix, and map visualization active."),
        ("Module 2: Demand Forecasting", "scikit-learn, statsmodels, pandas", "COMPLETE", "Dual-model engine (Ridge + Holt-Winters), auto R² scoring, what-if scenarios."),
        ("Module 3: Capacity Monitoring", "FastAPI, Pydantic, Python", "IN PROGRESS", "API schema & reserved routes created; live utilization logic & alerts pending."),
        ("Module 4: Campus Accessibility", "NetworkX (Dijkstra), Shapely", "IN PROGRESS", "Distance matrix served; isochrone polygons & bottleneck analysis pending."),
        ("Module 5: Facility Siting Optimizer", "PuLP (ILP Solver), NetworkX", "PENDING", "API routes reserved; mathematical p-median formulation & zoning rules to be wired."),
        ("Module 6: API & Web Dashboard", "FastAPI, Streamlit, Folium", "OPERATIONAL", "Decoupled full-stack architecture active; Modules 1 & 2 fully visualized.")
    ]

    for row_idx, (m_name, tech, status, state) in enumerate(rows_data, start=1):
        # Name
        c0 = table.cell(row_idx, 0)
        c0.text = m_name
        c0.text_frame.paragraphs[0].font.size = Pt(11)
        c0.text_frame.paragraphs[0].font.bold = True
        
        # Tech
        c1 = table.cell(row_idx, 1)
        c1.text = tech
        c1.text_frame.paragraphs[0].font.size = Pt(10)
        c1.text_frame.paragraphs[0].font.color.rgb = TEXT_MUTED

        # Status
        c2 = table.cell(row_idx, 2)
        c2.text = status
        p = c2.text_frame.paragraphs[0]
        p.font.size = Pt(11)
        p.font.bold = True
        if status in ["COMPLETE", "OPERATIONAL"]:
            p.font.color.rgb = SUCCESS
        elif status == "IN PROGRESS":
            p.font.color.rgb = PRIMARY
        else:
            p.font.color.rgb = WARNING

        # State
        c3 = table.cell(row_idx, 3)
        c3.text = state
        c3.text_frame.paragraphs[0].font.size = Pt(10)
        c3.text_frame.paragraphs[0].font.color.rgb = TEXT_DARK

    # =========================================================================
    # SLIDE 12: Summary & Expected Impact (Dark Theme)
    # =========================================================================
    s12 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s12, BG_DARK)

    tbox = s12.shapes.add_textbox(Inches(1.0), Inches(1.2), Inches(11.3), Inches(5.2))
    tf12 = tbox.text_frame
    tf12.word_wrap = True

    p = tf12.paragraphs[0]
    p.text = "Summary & Project Impact"
    p.font.size = Pt(32)
    p.font.bold = True
    p.font.color.rgb = TEXT_LIGHT
    p.space_after = Pt(20)

    impacts = [
        ("Proactive Capital Planning: ", "Transforms campus administration from reactive crisis management (building after severe shortages) to data-driven proactive expansion 3-5 years ahead."),
        ("Scientifically Defensible Decisions: ", "Provides administrative boards with mathematical justification (R² forecast accuracy & p-median distance minimization) for infrastructure investments."),
        ("Enhanced Student Wellbeing: ", "Minimizes daily walking fatigue and prevents chronic overcrowding in student residences, classrooms, and dining halls."),
        ("Extensible Smart-Campus Foundation: ", "The digitized GIS network graph and REST API establish a scalable foundation that can easily incorporate IoT smart-campus sensors in the future.")
    ]

    for title, desc in impacts:
        p = tf12.add_paragraph()
        p.space_after = Pt(14)
        r1 = p.add_run()
        r1.text = "✔ " + title
        r1.font.bold = True
        r1.font.size = Pt(14)
        r1.font.color.rgb = RGBColor(96, 165, 250) # Light Blue 400
        r2 = p.add_run()
        r2.text = desc
        r2.font.size = Pt(13)
        r2.font.color.rgb = RGBColor(226, 232, 240)

    p_end = tf12.add_paragraph()
    p_end.space_before = Pt(24)
    p_end.text = "Thank You! Questions & Discussion"
    p_end.font.size = Pt(20)
    p_end.font.bold = True
    p_end.font.color.rgb = TEXT_LIGHT

    # Save
    prs.save(output_path)
    print(f"Presentation saved successfully to: {output_path}")

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "PIPS_Project_Presentation.pptx"
    create_deck(out)
