# Airflow Data Pipelines

![License](https://img.shields.io/github/license/qazsedc13/airflow)
![Airflow Version](https://img.shields.io/badge/Airflow-2.6.1-blue)
![Python Version](https://img.shields.io/badge/Python-3.9-green)
![Docker](https://img.shields.io/badge/Docker-Compose-green)

Проект для локального запуска и разработки конвейеров данных (DAGs) с использованием Apache Airflow в Docker. Настроенная среда для оркестрации задач обработки данных с примерами интеграции API, S3 и базами данных.

---

## 🚀 Основные возможности

- **Оркестрация ETL**: Автоматизация задач извлечения, трансформации и загрузки данных.
- **Интеграция с внешними API**: Получение данных о курсах валют и других источников.
- **Работа с S3**: Примеры взаимодействия с Amazon S3 через boto3.
- **Поддержка БД**: Интеграция с PostgreSQL и SQLite для хранения результатов.
- **Паттерн Producer-Consumer**: Реализация асинхронной обработки данных.
- **Локальная разработка**: Полнофункциональная среда Airflow в Docker для быстрой разработки и тестирования DAG.

---

## 🛠 Технологический стек

- **Apache Airflow 2.6.1**: Оркестратор задач.
- **Docker & Docker Compose**: Контейнеризация инфраструктуры.
- **Python 3.9**: Среда исполнения для DAG.
- **PostgreSQL 13**: Основная база данных метаданных Airflow.
- **Redis**: Брокер сообщений для CeleryExecutor.
- **SQLite**: Лёгкая БД для примеров работы с данными.

### Ключевые зависимости (Python)
- `pandas`
- `boto3`
- `psycopg2`
- `apache-airflow==2.6.1`

---

## 📋 Предварительные требования

- **Docker Engine**: 20.10+
- **Docker Compose**: 2.0+
- **RAM**: Минимум 4GB свободного объема (рекомендуется 8GB для комфортной работы).
- **ОС**: Linux, macOS или Windows с WSL2.
- **Порт**: 8080 должен быть свободен.

---

## 🚀 Установка и запуск

### 1. Клонирование репозитория
```bash
git clone git@github.com:qazsedc13/airflow.git
cd airflow
```

### 2. Подготовка окружения
При необходимости создайте файл `.env` для специфической конфигурации:
```bash
echo "AIRFLOW__CORE__EXECUTOR=CeleryExecutor" > .env
```

### 3. Сборка и запуск
Запустите все сервисы (Airflow, PostgreSQL, Redis):
```bash
docker compose up -d
```

### 4. Доступ к интерфейсу
| Сервис | URL | Логин / Пароль |
| :--- | :--- | :--- |
| **Airflow Webserver** | [http://localhost:8080](http://localhost:8080) | `airflow` / `airflow` |

---

## 💡 Работа с проектом

### Примеры DAG

Помещайте ваши Python-скрипты в директорию `./dags`. Airflow автоматически обнаружит их.

#### Извлечение данных о курсах валют
DAG `dag.py` извлекает курсы валют (EUR/RUB) и данные из GitHub, сохраняя результаты в CSV и SQLite:
- Чтение данных из внешних API
- Парсинг и трансформация данных
- Сохранение в файловую систему и БД

#### Работа с Amazon S3
DAG `boto3_s3.py` демонстрирует взаимодействие с Amazon S3:
- Загрузка файлов в S3 bucket
- Чтение объектов из S3
- Управление доступом и версиями

#### Паттерн Producer-Consumer
Файлы `producer.py` и `consumer.py` реализуют асинхронную обработку данных:
- Producer генерирует сообщения/задания
- Consumer обрабатывает полученные данные

### Настройка подключений (Connections)

Для работы с внешними сервисами настройте Connections в Airflow:
1. Перейдите в **Admin → Connections**.
2. Добавьте новое подключение:
   - **PostgreSQL**: `postgres://user:password@host:5432/dbname`
   - **S3**: Укажите AWS Access Key и Secret Key
   - **HTTP**: Для API запросов

---

## 📁 Структура проекта

| Файл / Директория | Описание |
| :--- | :--- |
| `dags/` | Исходный код DAG-файлов |
| `docker-compose.yaml` | Конфигурация инфраструктуры (webserver, scheduler, worker, redis, postgres) |
| `.env` | Переменные окружения для настройки Airflow |
| `.gitignore` | Список игнорируемых файлов для Git |

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

**Ошибка инициализации базы данных:**
Если PostgreSQL не успела инициализироваться, выполните перезапуск:
```bash
docker compose restart postgres airflow-webserver
```

**Недостаточно памяти:**
При нехватке RAM (менее 4GB) сервисы могут завершаться аварийно. Освободите память или увеличьте лимит Docker.

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
