import unittest
from unittest.mock import patch, MagicMock
from weather import get_weather, WeatherData
import requests


class TestWeatherFunctions(unittest.TestCase):

    @patch('weather.requests.get')
    def test_get_weather(self, mock_get):
        
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'weather': [{'main': 'Clouds', 'description': 'scattered clouds', 'icon': '03d'}],
            'main': {'temp': -11, "feels_like": -17}
        }

        mock_get.return_value = mock_response

        city_name = 'Astana'
        weather_data = get_weather(city_name, 'dummy_api_key')

        self.assertEqual(weather_data.main, 'Clouds')
        self.assertEqual(weather_data.description, 'scattered clouds')
        self.assertEqual(weather_data.icon, '03d')
        self.assertEqual(weather_data.temperature, -11)
        self.assertEqual(weather_data.feels_like, -17)

    @patch('weather.requests.get')
    def test_get_weather_api_error(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = {'message': 'city'}
        
        mock_get.return_value = mock_response

        city_name = 'InvalidCity'

        with self.assertRaises(ValueError) as context:
            get_weather(city_name, 'dummy_api_key')

        self.assertIn("Invalid API response", str(context.exception))
    
    @patch('weather.requests.get')
    def test_get_weather_timeout(self, mock_get):
        mock_get.side_effect = requests.exceptions.Timeout
        
        city_name = 'Astana'

        with self.assertRaises(ValueError) as context:
            get_weather(city_name, 'dummy_api_key')

        self.assertIn("Timeout occurred", str(context.exception))



if __name__ == '__main__':
    unittest.main()