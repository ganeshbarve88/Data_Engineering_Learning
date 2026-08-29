from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2026, 6, 13),
    'retries': 1,
}

with DAG('pagila_to_bq_pipeline', 
         default_args=default_args, 
         schedule='@daily', # Runs once every day
         catchup=False) as dag:

    # Task 1: Run your extraction script
    extract_task = BashOperator(
        task_id='extract_from_psql',
        bash_command='python /opt/airflow/scripts/psql_extract_to_csv.py'
    )

    # Task 2: Load into BigQuery via dbt
    load_task = BashOperator(
        task_id='dbt_seed',
        bash_command='cd /opt/airflow/dbt_project && dbt seed'
    )

    extract_task >> load_task # Defines the dependency