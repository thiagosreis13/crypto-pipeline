from airflow import DAG
from datetime import datetime
from airflow.providers.standard.operators.python import PythonOperator
from crypto.pipeline import extract_load_dados

dag = DAG(
    'crypto',
    schedule = '@daily',
    max_active_runs=1,
    default_args={
        'owner': 'airflow',
        'retries': 1,
        'start_date': datetime(2023, 1, 1)
    },
    catchup=False,
    tags=["crypto","usd"]

)


extract_load_task = PythonOperator(
    task_id ='extract_load_crypto',
    python_callable=extract_load_dados,
    op_kwargs={"moeda": "usd", "qtd": "5", "destino":"top5_NovaVersao", "host":"host.docker.internal"},
    dag=dag
)