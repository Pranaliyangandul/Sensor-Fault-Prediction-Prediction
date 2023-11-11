from asyncio import tasks
import json
from textwrap import dedent
import pendulum
import os
from airflow import DAG
from airflow.operators.python import PythonOperator

with DAG(
    "sensor_training",
    default_args={'retries': 2},
    description='Sensor Fault Detection',
    schedule_interval="@weekly",
    start_date=pendulum.datetime(2023, 11, 11, tz="UTC"),
    catchup=False,
    tags=['example'],


) as dag:
    def start_training(**kwargs):
        from sensor.pipeline.training_pipeline import start_training_pipeline
        start_training_pipeline()

    def sync_artifact_to_s3_bucket(**kwargs):
        bucket_name=os.getenv("BUCKET_NAME")
        os.system(f"aws s3 sync /app/artifact s3://{bucket_name}/artifacts")
        os.system(f"aws s3 sync /app/saved_models s3://{bucket_name}/artifacts")

    training_pipeline=PythonOperator(
        task_id="training_pipeline",
        python_callable=start_training
    )

    start_s3_sync=PythonOperator(
        task_id="start_s3_sync",
        python_callable=sync_artifact_to_s3_bucket

    )

    training_pipeline >> start_s3_sync