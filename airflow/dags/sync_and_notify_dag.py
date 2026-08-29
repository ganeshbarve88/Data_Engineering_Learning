from airflow import DAG
from airflow.providers.airbyte.operators.airbyte import AirbyteTriggerSyncOperator
from airflow.operators.email import EmailOperator
from datetime import datetime, timedelta

# Default parameters applied to all tasks
default_args = {
    'owner': 'Barve_Studio',
    'depends_on_past': False,
    'email': ['colorfulkanasu@gmail.com'],
    'email_on_failure': True,   # Automatically sends email if any task fails
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Define DAG schedule and properties
with DAG(
    dag_id='pagila_airbyte_bronze_sync',
    default_args=default_args,
    description='Syncs Pagila Postgres to BigQuery Bronze via Airbyte on a schedule',
    schedule='0 6 * * *',  # Runs every day at 06:00 UTC (or use '@daily')
    start_date=datetime(2025, 1, 1),
    catchup=False,
    tags=['airbyte', 'bronze', 'ingestion'],
) as dag:

    # 1. Trigger Airbyte Ingestion
    trigger_airbyte_sync = AirbyteTriggerSyncOperator(
        task_id='trigger_airbyte_sync',
        airbyte_conn_id='airbyte_local',        # Airflow connection ID pointing to Airbyte
        connection_id='784fba74-fde6-4c04-80c8-9c51981d1499',  # The UUID from your Airbyte Connection URL
        asynchronous=False,                     # Waits for sync to complete before proceeding
        timeout=3600,                           # Timeout after 1 hour if stuck
    )

    # 2. Success Email Notification
    send_success_email = EmailOperator(
        task_id='send_success_email',
        to='ganeshbarve88@gmail.com,supriyabhide08@gmail.com',
        subject='✅ Ingestion Success: Pagila DB to BigQuery Bronze',
        html_content="""
        <h3>Airbyte Sync Completed Successfully!</h3>
        <p>The scheduled sync from <b>Local Pagila DB</b> to <b>BigQuery (Bronze Layer)</b> has finished.</p>
        <ul>
            <li><b>Execution Date:</b> {{ ds }}</li>
            <li><b>Status:</b> SUCCESS</li>
            <li><b>DAG:</b> {{ dag.dag_id }}</li>
        </ul>
        <p>Next step: Trigger dbt models for Silver & Gold transformation.</p>
        """,
    )

    # Define task execution order
    trigger_airbyte_sync >> send_success_email