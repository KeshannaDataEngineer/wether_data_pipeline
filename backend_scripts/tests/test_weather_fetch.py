import unittest
from unittest.mock import patch, MagicMock
from backend.weather_fetch import fetch_and_save_weather_data

class TestWeatherFetch(unittest.TestCase):
    
    @patch('backend.weather_fetch.requests.get')  
    def test_fetch_and_save_weather_data(self, mock_get):
      
        mock_response_data = {
            'hourly': {
                'temperature_2m': [25, 26, 27],
                'precipitation': [0, 0, 1],
            },
            'latitude': 52.52,
            'longitude': 13.41,
        }

       
        mock_get.return_value = MagicMock(status_code=200, json=MagicMock(return_value=mock_response_data))

       
        result = fetch_and_save_weather_data(1, '2024-10-01', '2024-10-02')

       
        self.assertIn('hourly', result)  
        self.assertEqual(result['hourly']['temperature_2m'], [25, 26, 27]) 
        self.assertEqual(result['hourly']['precipitation'], [0, 0, 1]) 
        
      
        mock_get.assert_called_once_with(
            'https://api.open-meteo.com/v1/forecast',
            params={
                'latitude': 52.52, 
                'longitude': 13.41,
                'start': '2024-10-01T00:00:00Z',
                'end': '2024-10-02T23:59:59Z',
                'hourly': 'temperature_2m,precipitation'
            }
        )

if __name__ == '__main__':
    unittest.main()
