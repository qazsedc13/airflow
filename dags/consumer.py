from airflow import DAG, Dataset
from airflow.decorators import task

from datetime import datetime

my_file = Dataset('/tmp/my_file.txt')

with DAG(
    dag_id='consumer',
    schedule=[my_file],
    start_date=datetime(2023, 1, 1),
    catchup=False

):

    @task
    def read_my_file():
        print("Сработало")
    
    read_my_file()