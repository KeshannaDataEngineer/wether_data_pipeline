import requests
from utils.api_utils import build_weather_api_url
from backend.pubsub_producer import publish_to_pubsub
from backend.gcs_temp_storage import store_in_gcs

def fetch_and_save_weather_data(venue_id: int, start_date: str, end_date: str) -> dict:
    try:
        
        api_url = build_weather_api_url(venue_id, start_date, end_date)
        
      
        response = requests.get(api_url)
        
       
        if response.status_code == 200:
            weather_data = response.json()

           
            publish_to_pubsub('weather-topic', weather_data)

            
            store_in_gcs('weather-temp-bucket', f'weather_data/{venue_id}_{start_date}_{end_date}.json', weather_data)

            return weather_data
        else:
            raise Exception(f"Failed to fetch weather data: {response.status_code}, {response.text}")

    except requests.exceptions.RequestException as e:
        raise Exception(f"Error during API request: {str(e)}")
