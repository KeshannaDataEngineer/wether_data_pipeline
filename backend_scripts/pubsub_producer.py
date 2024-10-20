from google.cloud import pubsub_v1

def publish_to_pubsub(topic_name: str, weather_data: dict) -> None:
    try:
      
        publisher = pubsub_v1.PublisherClient()
        
       
        topic_path = publisher.topic_path('your-project-id', topic_name)
        
        
        data = str(weather_data).encode('utf-8')
        
        
        future = publisher.publish(topic_path, data)
        
      
        future.result()  
        
        print(f"Published weather data to Pub/Sub topic: {topic_name}")

    except Exception as e:
        print(f"Failed to publish to Pub/Sub topic {topic_name}: {e}")
        raise 
