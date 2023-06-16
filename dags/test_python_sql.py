from __future__ import annotations

import logging
import shutil
import sys
import tempfile
import time
from pprint import pprint
from sqlalchemy import create_engine
import pendulum
import pandas as pd

from airflow import DAG
from airflow.decorators import task
from airflow.operators.python import ExternalPythonOperator, PythonVirtualenvOperator

log = logging.getLogger(__name__)

PATH_TO_PYTHON_BINARY = sys.executable

BASE_DIR = tempfile.gettempdir()


def x():
    pass


with DAG(
    dag_id="test",
    schedule=None,
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    catchup=False,
    tags=["test"],
) as dag:

    
    @task(task_id="con_db")
    def con_db():
        try:
            engine = create_engine("postgresql+psycopg2://qazsedc13:456321z@db:5432/qazsedc13")
        
        
            pprint(engine)

            df = pd.DataFrame({'a': [i for i in range(100)],
                               'b': [i for i in range(100)],
                               'c': [str(i) + 'c' for i in range(100)]})
            df.to_sql('test', engine, if_exists='replace', index=False)

            pprint(df.head(5))

        except Exception as e:
            pprint(repr(e))
        
        return "Whatever you return gets printed in the logs"

    run_this = con_db()
    
    
    run_this 