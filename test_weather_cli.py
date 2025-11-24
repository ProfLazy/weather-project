#!/usr/bin/env python3
"""
Basic tests for the weather CLI application.
"""

import unittest
from unittest.mock import patch, MagicMock
import requests
import weather_cli


class TestWeatherClient(unittest.TestCase):
    """Test the WeatherClient class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.api_key = "test_api_key_12345"
        self.client = weather_cli.WeatherClient(self.api_key)
    
    def test_init(self):
        """Test WeatherClient initialization."""
        self.assertEqual(self.client.api_key, self.api_key)
    
    @patch('weather_cli.requests.get')
    def test_get_weather_success(self, mock_get):
        """Test successful weather data retrieval."""
        # Mock successful API response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "name": "London",
            "sys": {"country": "GB"},
            "weather": [{"main": "Clear", "description": "clear sky"}],
            "main": {"temp": 15.5, "feels_like": 14.2, "temp_min": 14.0, "temp_max": 17.0, "humidity": 65, "pressure": 1013}
        }
        mock_get.return_value = mock_response
        
        result = self.client.get_weather("London")
        
        self.assertEqual(result["name"], "London")
        self.assertEqual(result["sys"]["country"], "GB")
        mock_get.assert_called_once()
    
    @patch('weather_cli.requests.get')
    def test_get_weather_invalid_api_key(self, mock_get):
        """Test handling of invalid API key."""
        # Mock 401 Unauthorized response
        mock_response = MagicMock()
        mock_response.status_code = 401
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("401 Unauthorized")
        mock_get.return_value = mock_response
        
        with self.assertRaises(ValueError) as context:
            self.client.get_weather("London")
        
        self.assertIn("Invalid API key", str(context.exception))
    
    @patch('weather_cli.requests.get')
    def test_get_weather_city_not_found(self, mock_get):
        """Test handling of city not found."""
        # Mock 404 Not Found response
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("404 Not Found")
        mock_get.return_value = mock_response
        
        with self.assertRaises(ValueError) as context:
            self.client.get_weather("InvalidCityXYZ")
        
        self.assertIn("not found", str(context.exception))


class TestFormatWeatherData(unittest.TestCase):
    """Test the format_weather_data function."""
    
    def test_format_weather_data_metric(self):
        """Test formatting weather data with metric units."""
        sample_data = {
            "name": "London",
            "sys": {"country": "GB"},
            "weather": [{"main": "Clear", "description": "clear sky"}],
            "main": {
                "temp": 15.5,
                "feels_like": 14.2,
                "temp_min": 14.0,
                "temp_max": 17.0,
                "humidity": 65,
                "pressure": 1013
            },
            "wind": {"speed": 3.5}
        }
        
        result = weather_cli.format_weather_data(sample_data, "metric")
        
        self.assertIn("London, GB", result)
        self.assertIn("Clear", result)
        self.assertIn("15.5°C", result)
        self.assertIn("Humidity: 65%", result)
        self.assertIn("3.5 m/s", result)
    
    def test_format_weather_data_imperial(self):
        """Test formatting weather data with imperial units."""
        sample_data = {
            "name": "New York",
            "sys": {"country": "US"},
            "weather": [{"main": "Rain", "description": "light rain"}],
            "main": {
                "temp": 68.0,
                "feels_like": 67.5,
                "temp_min": 65.0,
                "temp_max": 70.0,
                "humidity": 80,
                "pressure": 1015
            },
            "wind": {"speed": 5.5}
        }
        
        result = weather_cli.format_weather_data(sample_data, "imperial")
        
        self.assertIn("New York, US", result)
        self.assertIn("Rain", result)
        self.assertIn("68.0°F", result)
        self.assertIn("Humidity: 80%", result)


if __name__ == "__main__":
    unittest.main()
