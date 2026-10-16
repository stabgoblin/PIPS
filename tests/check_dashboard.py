"""Render all dashboard pages against the local module implementations."""
import sys
from pathlib import Path
from unittest.mock import patch
from streamlit.testing.v1 import AppTest
from src.api.main import health
from src.api.routers import campus_mapping as mapping, capacity_monitor as capacity, accessibility, facility_optimizer as optimizer, demand_forecast as forecast
from src.api.schemas import ForecastRequest
sys.path.insert(0, str(Path('src/dashboard').resolve()))
import api_client

GET = {
    '/api/health': health,
    '/api/mapping/buildings': mapping.get_buildings,
    '/api/mapping/paths': mapping.get_paths,
    '/api/mapping/center': mapping.get_center,
    '/api/mapping/buildings/summary': mapping.get_buildings_summary,
    '/api/mapping/graph/summary': mapping.get_graph_summary,
    '/api/capacity/facilities': capacity.list_facilities,
    '/api/capacity/thresholds': capacity.get_thresholds,
    '/api/accessibility/matrix': accessibility.distance_matrix,
    '/api/optimization/candidates': optimizer.candidate_sites,
    '/api/forecast/courses': forecast.list_courses,
    '/api/forecast/overview': forecast.department_overview,
    '/api/forecast/datasets': forecast.list_datasets,
}

def get(endpoint, params=None):
    return GET[endpoint]()

def post(endpoint, payload=None):
    assert endpoint == '/api/forecast/predict'
    return forecast.predict_demand(ForecastRequest(**payload))

with patch.object(api_client, 'get', get), patch.object(api_client, 'post', post):
    app = AppTest.from_file(str(Path('src/dashboard/app.py').resolve()), default_timeout=60).run()
    assert not app.exception, app.exception
    for page in ['Home', 'Campus Mapping', 'Student Demand Forecasting', 'Capacity & Threshold Monitoring', 'Campus Accessibility', 'Facility Location Optimization', 'API Status']:
        app.button(key='nav_system' if page == 'API Status' else f'nav_{page}').click().run()
        assert not app.exception, (page, app.exception)
        print('PASS:', page)
    app.button(key='nav_Home').click().run()
    app.button(key='open_Campus Mapping').click().run()
    assert app.session_state['navigation'] == 'Campus Mapping'
    assert not app.exception
    print('PASS: overview navigation')
with patch.object(api_client, 'get', return_value={'status': 'error', 'message': 'Offline', 'data': None}):
    for page in ['Home', 'Campus Mapping', 'Student Demand Forecasting', 'Capacity & Threshold Monitoring', 'Campus Accessibility', 'Facility Location Optimization', 'API Status']:
        app.button(key='nav_system' if page == 'API Status' else f'nav_{page}').click().run()
        assert not app.exception, (page, app.exception)
    print('PASS: offline states')

