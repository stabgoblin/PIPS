"""Regression checks for basic planning behavior; no live API required."""
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import networkx as nx
from fastapi import HTTPException

from src.api import services
from src.api.routers import accessibility, capacity_monitor, facility_optimizer
from src.api.schemas import PMedianRequest, ThresholdConfig
from src.forecast.engine import predict_demand
from src.gis.build_campus_graph import build_graph


class PlanningTests(unittest.TestCase):
    def test_shared_path_junctions(self):
        graph = build_graph()
        self.assertTrue(nx.has_path(graph, 'Boys Hostel A', 'Girls Hostel A'))
        self.assertFalse(nx.has_path(graph, 'Sports Complex', 'Girls Hostel A'))

    def test_threshold_persistence_and_missing_occupancy(self):
        features = [{'properties': {'name': 'Lab', 'type': 'academic', 'capacity': 100, 'occupancy': 85}},
                    {'properties': {'name': 'Unknown', 'type': 'academic', 'capacity': 100}},
                    {'properties': {'name': 'Zero', 'type': 'academic', 'capacity': 0, 'occupancy': 5}}]
        with tempfile.TemporaryDirectory() as folder, patch.object(services, 'THRESHOLDS_FILE', Path(folder) / 'rules.json'), patch.object(services, 'building_features', return_value=features):
            self.assertEqual(len(capacity_monitor.alerts()['data']['alerts']), 1)
            self.assertEqual(capacity_monitor.alerts()['data']['unknown_count'], 2)
            capacity_monitor.set_thresholds(ThresholdConfig(threshold=.9))
            self.assertEqual(services.thresholds()['default_threshold'], .9)
            self.assertEqual(len(capacity_monitor.alerts()['data']['alerts']), 0)
            capacity_monitor.set_thresholds(ThresholdConfig(facility_type='academic', threshold=.8))
            self.assertEqual(len(capacity_monitor.alerts()['data']['alerts']), 1)

    def test_optimizer_weighted_solution_and_disconnection(self):
        sites = [{'id': 'A', 'zone': 'undeveloped'}, {'id': 'B', 'zone': 'undeveloped'}]
        demand = [{'name': 'Hall', 'capacity': 10}, {'name': 'Lab', 'capacity': 1}]
        matrix = {'Hall': {'A': 10, 'B': 100}, 'Lab': {'A': 100, 'B': 10}}
        with patch.object(services, 'candidates', return_value=sites), patch.object(services, 'facilities', return_value=demand), patch.object(facility_optimizer, 'load_json', return_value=matrix), patch.object(services, 'save_json'):
            result = facility_optimizer.run_pmedian(PMedianRequest())['data']
            self.assertEqual(result['selected'][0]['id'], 'A')
            self.assertEqual(result['weighted_distance_m'], 200)
            with self.assertRaises(HTTPException):
                facility_optimizer.run_pmedian(PMedianRequest(p=3))
            with self.assertRaises(HTTPException):
                facility_optimizer.run_pmedian(PMedianRequest(candidate_ids=['missing']))
            matrix['Hall'] = {}
            with self.assertRaises(HTTPException):
                facility_optimizer.run_pmedian(PMedianRequest())

    def test_accessibility_gaps_and_budget(self):
        matrix = {'A': {'A': 0, 'B': 100}, 'B': {'B': 0, 'A': 100}, 'C': {'C': 0}}
        with patch.object(accessibility, 'load_json', return_value=matrix):
            self.assertEqual(len(accessibility.unreachable_pairs()['data']['gaps']), 2)
            result = accessibility.isochrones('A', minutes=1, speed_m_per_min=80)
            self.assertEqual(len(result['data']['reachable']), 1)

    def test_forecast_bounds_and_validation(self):
        result = predict_demand('cse', horizon_years=10, growth_multiplier=.5, model_type='regression')
        self.assertEqual(len(result['projections']), 10)
        for row in result['projections']:
            self.assertLessEqual(row['lower_bound'], row['projected_applicants'])
            self.assertLessEqual(row['projected_applicants'], row['upper_bound'])
        with self.assertRaises(ValueError):
            predict_demand('cse', horizon_years=0)


if __name__ == '__main__':
    unittest.main()
