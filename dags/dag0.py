from airflow import DAG
from datetime import timedelta, datetime
import pandas as pd
import sqlite3

from airflow.utils.dates import days_ago
from airflow.operators.python_operator import PythonOperator
from airflow.hooks.base import BaseHook
from airflow.providers.postgres.hooks.postgres import PostgresHook

from sqlalchemy import create_engine, text

CONN_ID_PKAP = 'pkap_247'
CONN_ID_KAP = 'kap_247'

def _get_engine(conn_id_str):
    connection = BaseHook.get_connection(conn_id_str)

    user = connection.login
    password = connection.password
    host = connection.host
    port = connection.port
    dbname = connection.schema
    return create_engine(f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{dbname}',
                         pool_pre_ping=True)



def extract_currency(date, table_name, **kwargs):
  engine_kap = _get_engine(CONN_ID_KAP)
  
  """
  Выгружаем курс валюты
  """
  url = f'https://api.exchangerate.host/timeseries?start_date={date[:10]}&end_date={date[:10]}&base=USD&format=csv'

  df = pd.read_csv(url)
  df.to_sql(table_name, schema='bp_247_chm' ,con=engine_kap, index=False, if_exists='append')


dag = DAG('dag0',
          schedule_interval=timedelta(days=1),
          start_date=datetime(2023, 1, 1)
          )

extract_currency = PythonOperator(
        task_id='extract_currency',
        python_callable=extract_currency,
        op_kwargs={
            'date': '{{ ds }}',
            'table_name': 'currency'},
        dag=dag
    )


extract_currency

  