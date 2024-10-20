import unittest
from unittest.mock import patch, MagicMock
from backend.gcs_temp_storage import store_in_gcs
import json

class TestGCSTempStorage(unittest.TestCase):

    @patch('google.cloud.storage.Client')
    def test_store_in_gcs(self, mock_storage_client):
       
        mock_client = MagicMock()
        mock_storage_client.return_value = mock_client
        mock_bucket = MagicMock()
        mock_client.bucket.return_value = mock_bucket
        mock_blob = MagicMock()
        mock_bucket.blob.return_value = mock_blob
        
      
        weather_data = {"temperature_2m": 25}
        
       
        store_in_gcs('weather-temp-bucket', 'weather_data/test.json', weather_data)
        
      
        mock_client.bucket.assert_called_once_with('weather-temp-bucket')
        
      
        mock_bucket.blob.assert_called_once_with('weather_data/test.json')
        
      
        mock_blob.upload_from_string.assert_called_once_with(
            json.dumps(weather_data), 
            content_type='application/json'  
        )

if __name__ == '__main__':
    unittest.main()
