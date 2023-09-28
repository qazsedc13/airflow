from airflow import DAG
from datetime import timedelta, datetime
import pandas as pd
import sqlite3

from airflow.utils.dates import days_ago
from airflow.operators.python_operator import PythonOperator
from airflow.hooks.base import BaseHook
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.providers.common.sql.sensors.sql import SqlSensor

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

def _success_criteria(record):
    return record


def _failure_criteria(record):
    return True if not record else False

def _print():
    print('Успешно')

dag = DAG('dag1',
          schedule_interval=timedelta(days=1),
          start_date=datetime(2022, 12, 28)
          )

waiting = SqlSensor(
        task_id="waiting",
        conn_id="kap_247",
        sql="""
        SELECT count(*) as cnt
        FROM bp_247_chm.currency
        where date("date") = date(to_date('{{ ds }}', 'YYYY-MM-DD') - '1 DAY'::interval)
        """,
        success=_success_criteria,
        failure=_failure_criteria,
        fail_on_empty=False,
        poke_interval=20,
        mode="reschedule",
        timeout=60 * 5,
    )

_print = PythonOperator(
        task_id='_print',
        python_callable=_print,
        dag=dag
    )
waiting >> _print

  