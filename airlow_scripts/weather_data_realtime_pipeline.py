from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago
from datetime import timedelta
from google.cloud import storage
from backend.weather_fetch import fetch_and_save_weather_data
from backend.pubsub_producer import publish_to_pubsub
from backend.gcs_temp_storage import store_in_gcs
from backend.dataflow_pipeline import run_pipeline
from datetime import datetime
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': days_ago(1), 
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'weather_data_realtime_pipeline',
    default_args=default_args,
    description='A real-time weather data pipeline with Pub/Sub, GCS, Dataflow, and BigQuery',
    schedule_interval='@hourly',
)

def fetch_store_weather_data(**kwargs):
    venue_id = kwargs.get('venue_id', 1) 
    start_date = kwargs.get('start_date', '2024-10-01')  
    end_date = kwargs.get('end_date', '2024-10-02')  
    
   
    weather_data = fetch_and_save_weather_data(venue_id, start_date, end_date)
    
    if weather_data: 
      
        publish_to_pubsub('weather-topic', weather_data)
        
       
        store_in_gcs('weather-temp-bucket', f'weather_data/{venue_id}_{start_date}_{end_date}.json', weather_data)

       
        kwargs['ti'].xcom_push(key='weather_data', value=weather_data)
    else:
        raise ValueError("No weather data fetched!")


def trigger_dataflow(**kwargs):
  
    ti = kwargs['ti']
    weather_data = ti.xcom_pull(task_ids='fetch_store_weather_data', key='weather_data')

    if weather_data:
      
        run_pipeline(weather_data)
    else:
        raise ValueError("No weather data available for Dataflow pipeline!")


def cleanup_temp_files(**kwargs):
    client = storage.Client()
    bucket_name = 'weather-temp-bucket' 
    retention_days = 7  
    threshold_date = datetime.now() - timedelta(days=retention_days)

    bucket = client.bucket(bucket_name)
    blobs = bucket.list_blobs() 

    for blob in blobs:
       
        if blob.time_created < threshold_date:
            print(f"Deleting blob: {blob.name}")
            blob.delete() 
        else:
            print(f"Keeping blob: {blob.name}")


fetch_store_task = PythonOperator(
    task_id='fetch_store_weather_data',
    python_callable=fetch_store_weather_data,
    op_kwargs={'venue_id': 1, 'start_date': '2024-10-01', 'end_date': '2024-10-02'},  
    provide_context=True,  
    dag=dag,
)

trigger_dataflow_task = PythonOperator(
    task_id='trigger_dataflow_pipeline',
    python_callable=trigger_dataflow,
    provide_context=True,  
    dag=dag,
)

cleanup_task = PythonOperator(
    task_id='cleanup_temp_files',
    python_callable=cleanup_temp_files,
    dag=dag,
)

fetch_store_task >> trigger_dataflow_task >> cleanup_task
