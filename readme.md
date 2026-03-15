# Airflow Data Pipelines

Проект для локального запуска и разработки конвейеров данных (DAGs) с использованием Apache Airflow в Docker.

## Описание
Данный проект предоставляет настроенную среду Apache Airflow для оркестрации задач обработки данных. Включены примеры DAG, которые выполняют извлечение данных о курсах валют из внешних API, работу с S3 (boto3), а также взаимодействие с базами данных PostgreSQL и SQLite.

## Технологический стек
- **Оркестрация:** Apache Airflow 2.6.1
- **Контейнеризация:** Docker, Docker Compose
- **Язык программирования:** Python 3.9
- **Базы данных:** PostgreSQL 13 (основная БД Airflow), SQLite (для примеров)
- **Брокер сообщений:** Redis (для CeleryExecutor)
- **Библиотеки Python:** Pandas, Boto3, Psycopg2

## Установка и запуск

1. Убедитесь, что у вас установлены **Docker** и **Docker Compose**.
2. Склонируйте репозиторий:
   ```bash
   git clone git@github.com:qazsedc13/airflow.git
   ```
   И перейдите в папку проекта.
3. Подготовьте файл `.env` (если требуется специфическая конфигурация).
4. Запустите сервисы:
   ```bash
   docker-compose up -d
   ```
5. После запуска Airflow будет доступен по адресу: [http://localhost:8080](http://localhost:8080)
   - Логин по умолчанию: `airflow`
   - Пароль по умолчанию: `airflow`

## Примеры использования
В папке `dags/` содержатся примеры рабочих процессов:
- `dag.py`: Извлекает курсы валют (EUR/RUB) и данные из GitHub, сохраняя их в CSV и SQLite.
- `boto3_s3.py`: Пример взаимодействия с Amazon S3.
- `producer.py` и `consumer.py`: Примеры реализации паттерна Producer-Consumer в Airflow.

## Структура проекта
- `dags/` — директория с исходным кодом DAG-файлов.
- `docker-compose.yaml` — конфигурация Docker-контейнеров (webserver, scheduler, worker, redis, postgres).
- `.env` — файл с переменными окружения.
- `.gitignore` — список игнорируемых файлов для Git.

## Зависимости и требования
- Docker Engine 20.10.0+
- Docker Compose v2.0.0+
- Минимум 4 ГБ оперативной памяти для стабильной работы Airflow.
