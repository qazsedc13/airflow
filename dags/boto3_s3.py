import boto3

from airflow import DAG, Dataset
from airflow.decorators import task

from datetime import datetime

with DAG(
    dag_id='boto3_test',
    schedule='@once',
    start_date=datetime(2023, 1, 1),
    catchup=False,
    tags=['test', 'boto3']


):
    session = boto3.session.Session()
    s3 = session.client(
        service_name='s3',
        endpoint_url='http://s3server:8000'
    )

    bucket = 'from-sdex'
    # # Создать новый бакет
    # s3.create_bucket(Bucket='from-sdex')

    # # Загрузить объекты в бакет

    ## Из строки
    s3.put_object(Bucket=bucket, Key='object_name', Body='TEST', StorageClass='COLD')

    # ## Из файла
    # s3.upload_file('this_script.py', bucket, 'py_script.py')
    # s3.upload_file('this_script.py', bucket, 'script/py_script.py')

    # Получить список объектов в бакете
    for key in s3.list_objects(Bucket=bucket)['Contents']:
        print(key['Key'])

    # # Удалить несколько объектов
    # forDeletion = [{'Key':'object_name'}, {'Key':'script/py_script.py'}]
    # response = s3.delete_objects(Bucket=bucket, Delete={'Objects': forDeletion})

    # # Получить объект
    # get_object_response = s3.get_object(Bucket=bucket,Key='py_script.py')
    # print(get_object_response['Body'].read())