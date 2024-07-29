import unittest
from flask import json
from app import app  # Import the Flask app

class WeatherApiTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_get_weather(self):
        # Test GET /api/weather with no parameters
        response = self.app.get('/api/weather/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('application/json', response.content_type)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)

        # Test GET /api/weather with date filter
        response = self.app.get('/api/weather/?date=2024-07-29')
        self.assertEqual(response.status_code, 200)
        self.assertIn('application/json', response.content_type)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)
        
        # Test GET /api/weather with station_id filter
        response = self.app.get('/api/weather/?station_id=station_1')
        self.assertEqual(response.status_code, 200)
        self.assertIn('application/json', response.content_type)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)
        
        # Test pagination
        response = self.app.get('/api/weather/?page=1&per_page=5')
        self.assertEqual(response.status_code, 200)
        self.assertIn('application/json', response.content_type)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)

    def test_get_weather_stats(self):
        # Test GET /api/weather/stats with no parameters
        response = self.app.get('/api/weather/stats')
        self.assertEqual(response.status_code, 200)
        self.assertIn('application/json', response.content_type)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)

        # Test GET /api/weather/stats with date filter
        response = self.app.get('/api/weather/stats?date=2024-07-29')
        self.assertEqual(response.status_code, 200)
        self.assertIn('application/json', response.content_type)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)
        
        # Test GET /api/weather/stats with station_id filter
        response = self.app.get('/api/weather/stats?station_id=station_1')
        self.assertEqual(response.status_code, 200)
        self.assertIn('application/json', response.content_type)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)
        
        # Test pagination
        response = self.app.get('/api/weather/stats?page=1&per_page=5')
        self.assertEqual(response.status_code, 200)
        self.assertIn('application/json', response.content_type)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)

if __name__ == '__main__':
    unittest.main()
