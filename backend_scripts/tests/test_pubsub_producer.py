import unittest
from unittest.mock import patch, MagicMock
from backend.pubsub_producer import publish_to_pubsub

class TestPubSubProducer(unittest.TestCase):
    @patch('google.cloud.pubsub_v1.PublisherClient')
    def test_publish_to_pubsub(self, mock_publisher_client):
       
        mock_client = MagicMock()
        mock_publisher_client.return_value = mock_client
        
      
        weather_data = {"temperature_2m": 25}
        topic_name = 'weather-topic'
        
        
        publish_to_pubsub(topic_name, weather_data)
        
       
        mock_client.topic_path.assert_called_once_with('your-project-id', topic_name) 
        mock_client.publish.assert_called_once()  

       
        args, _ = mock_client.publish.call_args
        published_data = args[1] 
        self.assertEqual(published_data, weather_data)

if __name__ == '__main__':
    unittest.main()
