from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.hooks.base import BaseHook
from datetime import datetime
import psycopg2
import csv
import os

def load_csv_to_raw(**context):
    dag_run_conf = context['dag_run'].conf
    filename = dag_run_conf.get('filename')
    filepath = f"/opt/airflow/csv_data/{filename}"
    
    # Define schema and fully qualified table name
    schema_name = "family_fin_details_raw"
    table_base = filename.split('.')[0]
    raw_table = f"raw_{table_base}"
    full_table_name = f"{schema_name}.{raw_table}"
    
    # Read the CSV header
    with open(filepath, 'r') as f:
        import csv
        reader = csv.reader(f)
        headers = next(reader)
        
    safe_headers = [h.replace('\ufeff', '').strip().lower().replace(' ', '_') for h in headers]
    columns_sql = ", ".join([f"{col} TEXT" for col in safe_headers])
    
    # Define SQL statements
    create_schema_sql = f"CREATE SCHEMA IF NOT EXISTS {schema_name};"
    create_table_sql = f"CREATE TABLE IF NOT EXISTS {full_table_name} ({columns_sql});"

    from airflow.hooks.base import BaseHook
    import psycopg2
    db_conn = BaseHook.get_connection("my_postgres_conn")
    conn = psycopg2.connect(
        host=db_conn.host,
        dbname=db_conn.schema,
        user=db_conn.login,
        password=db_conn.password,
        port=db_conn.port
    )
    cursor = conn.cursor()
    
    try:
        # Execute schema creation first, then table, then truncate
        cursor.execute(create_schema_sql)
        cursor.execute(create_table_sql)
        cursor.execute(f"TRUNCATE TABLE {full_table_name};")
        
        with open(filepath, 'r') as f:
            next(f) 
            cursor.copy_expert(f"COPY {full_table_name} FROM STDIN WITH CSV", f)
            
        conn.commit()
        print(f"Successfully loaded data into {full_table_name}")
        
    except Exception as e:
        conn.rollback()
        print(f"Failed to load {filename}: {e}")
        raise e
        
    finally:
        cursor.close()
        conn.close()

with DAG(
    dag_id='csv_scd2_pipeline',
    start_date=datetime(2023, 1, 1),
    schedule=None, 
    catchup=False
) as dag:

    # The dbt task is removed for this testing phase. 
    # Only the raw loading task will execute.
    load_raw_task = PythonOperator(
        task_id='load_csv_to_raw',
        python_callable=load_csv_to_raw
    )