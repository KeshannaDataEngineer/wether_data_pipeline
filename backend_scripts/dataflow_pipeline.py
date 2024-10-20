import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
from google.cloud import bigquery

class ValidateWeatherData(beam.DoFn):
    def process(self, element):
       
        if -100 < element['temperature_2m'] < 100:
            yield element
        else:
            print(f"Invalid data: {element}")

class FormatForBigQuery(beam.DoFn):
    def process(self, element):
       
        yield {
            'venue_id': element['venue_id'],
            'timestamp': element['timestamp'],
            'temperature_2m': element['temperature_2m'],
            'humidity': element['relative_humidity_2m'],
            'dewpoint': element['dewpoint_2m'],
            'apparent_temperature': element['apparent_temperature'],
            'precipitation_probability': element['precipitation_probability'],
            'rain': element['rain'],
            'snowfall': element['snowfall']
        }

def run_pipeline():
    project_id = 'your-gcp-project-id'
    dataset_id = 'weather_dataset'
    table_id = 'weather_data'

    options = PipelineOptions(
        project=project_id,
        region='us-central1',
        runner='DataflowRunner',
        temp_location='gs://your-temp-bucket/temp/',
        staging_location='gs://your-temp-bucket/staging/'
    )

    with beam.Pipeline(options=options) as p:
        (p
         | 'Read from PubSub' >> beam.io.ReadFromPubSub(topic='projects/your-gcp-project-id/topics/weather-topic')
         | 'Parse JSON' >> beam.Map(lambda x: json.loads(x.decode('utf-8')))
         | 'Validate Data' >> beam.ParDo(ValidateWeatherData())
         | 'Format for BigQuery' >> beam.ParDo(FormatForBigQuery())
         | 'Write to BigQuery' >> beam.io.WriteToBigQuery(
                table=f'{project_id}:{dataset_id}.{table_id}',
                schema='SCHEMA_AUTODETECT',
                write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND
            ))
