# Weather Data Pipeline

This project implements an end-to-end weather data pipeline that fetches weather data from an external API, processes the data, and stores it in Google Cloud services. It uses the following technologies:
- Google Cloud Platform (GCP)
- Apache Airflow for orchestration
- Google Pub/Sub for messaging
- Google Cloud Storage for temporary data storage
- Google Cloud Dataflow for data processing
- Google BigQuery for data analytics

## Project Structure

weather-data-pipeline/
│
├── airflow_dags/
│   └── weather_data_realtime_pipeline.py    
│
├── backend/
│   ├── __init__.py                           
│   ├── weather_fetch.py                   
│   ├── pubsub_producer.py                   
│   ├── dataflow_pipeline.py                
│   ├── bigquery_loader.py                   
│   └── tests/
│       ├── test_weather_fetch.py             
│       ├── test_pubsub_producer.py           
│       └── test_dataflow_pipeline.py        
│
├── utils/
│   ├── __init__.py                           
│   ├── api_utils.py                         
│   ├── db_utils.py                          
│   ├── logging_utils.py                     
│
├── cloudbuild.yaml                           
├── Dockerfile                                
├── requirements.txt                          
├── README.md                        


## Prerequisites

- A Google Cloud Platform (GCP) account.
- Google Cloud SDK installed and configured on your machine.
- Docker installed on your machine.
- Python 3.9 or higher installed.

## Setup Instructions

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your_username/weather_data_pipeline.git
   cd weather_data_pipeline

Create a Virtual Environment
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

Install Required Packages: Install the dependencies listed in requirements.txt.
pip install -r requirements.txt

Configure Google Cloud Services:

Create a Pub/Sub topic named weather-topic.
Create a Google Cloud Storage bucket named weather-temp-bucket.
Create a BigQuery dataset and table to store processed weather data.
Ensure that the Google Cloud credentials are set up properly on your machine.

API Endpoints
Fetch and Save Weather Data
Endpoint: /fetch_weather
Method: POST

{
  "venue_id": 1,
  "start_date": "2024-10-01",
  "end_date": "2024-10-02"
}

Response:
Success: 200 OK
Error: 400 Bad Request

Example using curl
curl -X POST http://localhost:8080/fetch_weather -H "Content-Type: application/json" -d '{"venue_id": 1, "start_date": "2024-10-01", "end_date": "2024-10-02"}'

Testing
Unit tests for each module are provided in the tests directory. To run the tests, execute:
python -m unittest discover -s tests

Deployment
Build and Deploy to Google Cloud Run
Make the Deployment Script Executable:

chmod +x deploy.sh

Run the Deployment Script:

./deploy.sh

This will build the Docker image, push it to Google Container Registry, and deploy it to Google Cloud Run.

Airflow DAG Configuration
The weather_data_pipeline.py file contains the Airflow DAG definition that orchestrates the data pipeline. It includes tasks for:

Fetching weather data from the API.
Publishing the data to Pub/Sub.
Storing the data in Google Cloud Storage.
Triggering the Dataflow pipeline for processing.
Cleaning up temporary files in GCS.
Schedule
The DAG is scheduled to run hourly, but you can adjust the schedule as needed.

Conclusion
This project provides a comprehensive solution for fetching, processing, and storing weather data using Google Cloud technologies. Feel free to explore and modify the project according to your needs. For further questions, please refer to the documentation or reach out for assistance.




