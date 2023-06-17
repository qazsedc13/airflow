# Первый запуск
## Создаём папки
mkdir -p ./dags ./logs ./plugins
echo -e "AIRFLOW_UID=$(id -u)" > .env

## Запускаем инициализацию
docker compose up airflow-init

### Должен быть такой вывод
airflow-init_1       | Upgrades done
airflow-init_1       | Admin user airflow created
airflow-init_1       | 2.5.0
start_airflow-init_1 exited with code 0


## Запуск сервиса
docker-compose up

## Остановка
docker-compose down --volumes --rmi all

# Комментарии и полезные ссылки

О том как использовать датасет как сенсор при обновлении таблицы в базе
https://stackoverflow.com/questions/75869048/how-to-use-a-table-as-dataset-for-airflow-in-data-aware-scheduling

запуск одного дага по факту
    обновления кого-нибудь темпового файла
    Информация отсюда: https://youtu.be/kPI2mPs-eQA
