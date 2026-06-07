
  dags/movielens_dag.py — Airflow оркестрирует всё по порядку
  Копировать
  from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import sys
sys.path.insert(0, "/opt/airflow")

from utils.extract import download_movielens
from utils.transform import run as run_transform

default_args = {
    "owner": "zhansaya",
    "retries": 1,
    "retry_delay": timedelta(minutes=3),
    "start_date": datetime(2024, 1, 1),
}

def validate_raw(**context):
    """Check that CSVs exist and are not empty."""
    import os, pandas as pd
    for fname in ["movies.csv", "ratings.csv"]:
        path = f"data/raw/{fname}"
        assert os.path.exists(path), f"Missing file: {path}"
        df = pd.read_csv(path)
        assert len(df) > 0, f"Empty file: {fname}"
        print(f"{fname}: {len(df)} rows OK")

with DAG(
    dag_id="movielens_etl",
    default_args=default_args,
    schedule_interval="@weekly",
    catchup=False,
    tags=["etl", "movies", "demo"],
    description="ETL pipeline for MovieLens dataset"
) as dag:

    extract = PythonOperator(
        task_id="extract_dataset",
        python_callable=download_movielens,
    )

    validate = PythonOperator(
        task_id="validate_raw_files",
        python_callable=validate_raw,
    )

    transform_load = PythonOperator(
        task_id="transform_and_load",
        python_callable=run_transform,
    )

    extract >> validate >> transform_load
  DAG — это граф задач. Airflow запускает их в правильном порядке: сначала extract, потом validate (проверяем что файлы скачались), только потом transform_and_load. Если какой-то шаг упал — следующий не запустится. Это и есть оркестрация.
