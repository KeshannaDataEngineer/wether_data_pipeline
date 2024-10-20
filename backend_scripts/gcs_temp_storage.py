from google.cloud import storage
import json

def store_in_gcs(bucket_name, file_path, weather_data):
    try:
       
        client = storage.Client()
        
       
        bucket = client.bucket(bucket_name)
        
       
        blob = bucket.blob(file_path)
        
       
        blob.upload_from_string(data=json.dumps(weather_data), content_type='application/json')
        
        print(f"Stored weather data in GCS: {bucket_name}/{file_path}")

    except Exception as e:
        print(f"Failed to store weather data in GCS: {e}")
        raise  
