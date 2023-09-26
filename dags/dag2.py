# Решение здесь
from airflow import DAG
from datetime import timedelta, datetime
import pandas as pd
import sqlite3

from airflow.utils.dates import days_ago
from airflow.operators.python_operator import PythonOperator

CONN = sqlite3.connect('example.db')



def extract_currency(date, csv_file, table_name, con=CONN, **kwargs):
  """
  Выгружаем курс валюты
  """
  url = f'https://api.exchangerate.host/timeseries?start_date={date[:10]}&end_date={date[:10]}&base=EUR&format=csv'

  df = pd.read_csv(url)
#   df.to_sql(table_name, con, index=False, if_exists='replace')
  df.to_csv(csv_file + date[:10] + '.csv', index=False)
  val = df.loc[df['code'] == 'RUB', 'rate'].items()
  kwargs['ti'].xcom_push(key='return value', value='val1')

def extract_data(date, csv_file, table_name, con=CONN):
  """
  Выгружаем файл
  """
  url = 'https://raw.githubusercontent.com/dm-novikov/stepik_airflow_course/main/data_new/' + date[:10] + '.csv'
  df = pd.read_csv(url, sep=',', encoding='utf-8')
  df.to_sql(table_name, con, index=False, if_exists='replace')
  df.to_csv(csv_file + date[:10] +'.csv', index=False)


dag = DAG('dag',
          schedule_interval=timedelta(days=1),
          start_date=datetime(2021, 1, 1),
          end_date=datetime(2021, 1, 4))

extract_currency = PythonOperator(
        task_id='extract_currency',
        python_callable=extract_currency,
        op_kwargs={
            'date': '{{ ds }}',
            'csv_file': '/root/airflow/currency',
            'table_name': 'currency'},
        dag=dag
    )

extract_data = PythonOperator(
        task_id='extract_data',
        python_callable=extract_data,
        op_kwargs={
            'date': '{{ ds }}',
            'csv_file': '/root/airflow/data',
            'table_name': 'data'},
        dag=dag
    )

extract_data >> extract_currency