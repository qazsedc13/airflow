# Airflow + Minio Data Pipelines

![License](https://img.shields.io/github/license/qazsedc13/airflow)
![Airflow Version](https://img.shields.io/badge/Airflow-2.6.3-blue)
![Python Version](https://img.shields.io/badge/Python-3.9-green)
![Minio](https://img.shields.io/badge/Minio-latest-red)
![Docker](https://img.shields.io/badge/Docker-Compose-green)

Проект для разработки ETL-конвейеров данных с использованием Apache Airflow и Minio в Docker. Интеграция объектного хранилища Minio для работы с файлами в формате S3 с загрузкой данных в PostgreSQL.

---

## 🚀 Основные возможности

- **ETL из S3 в PostgreSQL**: Автоматизация загрузки данных из объектного хранилища в реляционную БД.
- **Интеграция Minio**: Локальное S3-совместимое хранилище для разработки и тестирования.
- **Работа с s3fs**: Чтение файлов напрямую из S3 через файловую систему.
- **Обработка в памяти**: Загрузка данных без промежуточных файлов с использованием chunking.
- **Airflow Operators**: Использование встроенных операторов `S3ToSqlOperator` для трансфера данных.
- **Полный стек Airflow**: CeleryExecutor с worker, scheduler, triggerer и flower для мониторинга.

---

## 🛠 Технологический стек

- **Apache Airflow 2.6.3**: Оркестратор задач с CeleryExecutor.
- **Minio**: S3-совместимое объектное хранилище.
- **PostgreSQL 13**: База данных метаданных Airflow и целевая БД для ETL.
- **Redis**: Брокер сообщений для Celery.
- **Python 3.9**: Среда исполнения для DAG.
- **Docker & Docker Compose**: Контейнеризация инфраструктуры.

### Ключевые зависимости (Python)
- `s3fs`
- `pandas`
- `apache-airflow==2.6.3`
- `apache-airflow-providers-amazon`

---

## 📋 Предварительные требования

- **Docker Engine**: 20.10+
- **Docker Compose**: 2.0+
- **RAM**: Минимум 4GB (рекомендуется 8GB для CeleryExecutor).
- **ОС**: Linux, macOS или Windows с WSL2.
- **Порты**: 8080, 9000, 9090, 5432, 5433, 6379 должны быть свободны.

---

## 🚀 Установка и запуск

### 1. Клонирование репозитория
```bash
git clone git@github.com:qazsedc13/airflow.git
cd airflow
git checkout airflow-minio
```

### 2. Сборка и запуск
Запустите все сервисы (Airflow, Minio, PostgreSQL, Redis):
```bash
docker compose up -d --build
```

### 3. Доступ к интерфейсам
| Сервис | URL | Логин / Пароль |
| :--- | :--- | :--- |
| **Airflow Webserver** | [http://localhost:8080](http://localhost:8080) | `airflow` / `airflow` |
| **Minio Console** | [http://localhost:9090](http://localhost:9090) | `admin` / `Secure123$` |
| **Minio API** | [http://localhost:9000](http://localhost:9000) | `admin` / `Secure123$` |
| **PostgreSQL (Airflow)** | `localhost:5432` | `airflow` / `airflow` |
| **PostgreSQL (Target)** | `localhost:5433` | `kap_247_db` / `kap_247_db` |
| **Flower (Celery)** | [http://localhost:5555](http://localhost:5555) | — |

---

## 💡 Работа с проектом

### Настройка Minio

1. Войдите в Minio Console по адресу `http://localhost:9090`.
2. Создайте bucket для ваших данных:
   ```bash
   aws --endpoint-url http://localhost:9000 s3 mb s3://my-bucket
   ```
3. Загрузите файлы в bucket:
   ```bash
   aws --endpoint-url http://localhost:9000 s3 cp file.csv s3://my-bucket/file.csv
   ```

### Примеры DAG

Помещайте ваши Python-скрипты в директорию `./dags`. Airflow автоматически обнаружит их.

#### Загрузка из S3 в PostgreSQL с s3fs
DAG `s3_to_postgres_use_pandas_and_s3fs.py` читает данные из Minio через s3fs и загружает в PostgreSQL с использованием pandas:
- Подключение к S3 через s3fs
- Чтение CSV/Parquet файлов в DataFrame
- Вставка данных в PostgreSQL через SQLAlchemy

#### Загрузка с обработкой в памяти
DAG `s3_to_postgres_file_in_memory_chank.py` демонстрирует загрузку данных без сохранения на диск:
- Чтение файла из S3 в память
- Обработка данных chunk'ами для экономии памяти
- Потоковая вставка в БД

#### Использование S3ToSqlOperator
DAG `s3_to_postgres_use_operator_S3ToSqlOperator.py` использует встроенный оператор Airflow:
- Настройка S3ToSqlOperator для трансфера данных
- Автоматическое создание таблиц в целевой БД
- Поддержка различных форматов файлов

### Настройка подключений (Connections)

Для работы с Minio и PostgreSQL настройте Connections в Airflow:

1. Перейдите в **Admin → Connections**.
2. Добавьте подключение к Minio:
   - **Conn Id**: `minio_default`
   - **Conn Type**: `AWS`
   - **Key**: `admin`
   - **Secret**: `Secure123$`
   - **Host**: `http://minio:9000`
3. Добавьте подключение к целевой PostgreSQL:
   - **Conn Id**: `postgres_target`
   - **Conn Type**: `Postgres`
   - **Host**: `db_kap`
   - **Port**: `5432`
   - **Database**: `kap_247_db`
   - **User**: `kap_247_db`
   - **Password**: `kap_247_db`

---

## 📁 Структура проекта

| Файл / Директория | Описание |
| :--- | :--- |
| `dags/` | Исходный код DAG-файлов для ETL из S3 в PostgreSQL |
| `docker-compose.yaml` | Конфигурация инфраструктуры (9 сервисов) |
| `Dockerfile` | Кастомный образ Airflow с зависимостями |
| `requirements.txt` | Список Python-пакетов (s3fs) |

---

## 🔧 Управление инфраструктурой

**Остановка всех сервисов:**
```bash
docker compose down
```

**Просмотр логов:**
```bash
docker compose logs -f
```

**Запуск с профилем Flower:**
```bash
docker compose --profile flower up -d
```

**Полный сброс данных:**
```bash
docker compose down -v
```

**Перезапуск конкретных сервисов:**
```bash
docker compose restart airflow-webserver airflow-scheduler
```

**Просмотр состояния контейнеров:**
```bash
docker compose ps
```

---

## ⚠️ Устранение неполадок

**Airflow не запускается:**
Убедитесь, что контейнеры находятся в состоянии `healthy`. Проверить статус можно командой `docker compose ps`.

**Ошибка подключения к Minio:**
Проверьте, что сервис `minio` запущен и доступен по порту 9000. Убедитесь, что credentials указаны верно.

**S3ToSqlOperator не находит файлы:**
Убедитесь, что bucket существует и файлы загружены. Проверьте Conn Id подключения в настройках оператора.

**Недостаточно памяти:**
При нехватке RAM (менее 4GB) сервисы Celery могут завершаться аварийно. Увеличьте лимит Docker или отключите flower.

**DAG не отображается в интерфейсе:**
- Проверьте синтаксис Python-кода в файле DAG.
- Убедитесь, что файл имеет расширение `.py`.
- Перезапустите scheduler: `docker compose restart airflow-scheduler`.

---

## 📄 Лицензия

Проект распространяется под лицензией **MIT**.

---

## 📬 Контакты

- **Автор**: [qazsedc13](https://github.com/qazsedc13)
- **Репозиторий**: [airflow](https://github.com/qazsedc13/airflow)
- **Ветка**: `airflow-minio`
