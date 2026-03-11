# Task Manager API

REST API для управления задачами, построенный на **FastAPI** + **PostgreSQL**. Поддерживает создание, просмотр, обновление и удаление задач с фильтрацией и сортировкой.

---

## Структура проекта

```
TestTaskManager/
├── app/
│   ├── __init__.py
│   ├── config.py        # Настройки приложения (pydantic-settings)
│   ├── database.py      # Async SQLAlchemy движок и сессии
│   ├── models.py        # ORM-модель Task
│   ├── schemas.py       # Pydantic-схемы (Request / Response)
│   ├── main.py          # Точка входа FastAPI, lifespan
│   └── routers/
│       ├── __init__.py
│       └── tasks.py     # Все эндпоинты /tasks
├── .env.example
├── .gitignore
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── README.md
```

---

## Быстрый старт

### 1. Скопируйте `.env`

```bash
cp .env.example .env
```

> Файл `.env` уже содержит корректные значения для запуска через Docker Compose. При необходимости отредактируйте пароли.

### 2. Запустите через Docker Compose

```bash
docker-compose up --build -d
```

Команда запустит два сервиса:

| Сервис | Описание                           |
|--------|------------------------------------|
| `db`   | PostgreSQL 15 на порту 5432        |
| `api`  | FastAPI-приложение на порту 8000   |

При первом запуске сервис `api` автоматически создаёт таблицы в базе данных через `Base.metadata.create_all`.

### 3. Откройте Swagger UI

```
http://localhost:8000/docs
```

Там можно протестировать все эндпоинты прямо из браузера.

---

## Эндпоинты

| Метод    | URL                  | Описание                                  |
|----------|----------------------|-------------------------------------------|
| `POST`   | `/tasks`             | Создать задачу                            |
| `GET`    | `/tasks`             | Список задач (фильтр + сортировка)        |
| `GET`    | `/tasks/{task_id}`   | Получить задачу по ID                     |
| `PATCH`  | `/tasks/{task_id}`   | Частичное обновление задачи               |
| `DELETE` | `/tasks/{task_id}`   | Удалить задачу                            |

### Query-параметры для `GET /tasks`

| Параметр | Тип    | Возможные значения              | По умолчанию |
|----------|--------|---------------------------------|--------------|
| `status` | string | `todo`, `in_progress`, `done`   | —            |
| `sort`   | string | `asc`, `desc`                   | `desc`       |

**Пример:**
```
GET /tasks?status=todo&sort=asc
```

---

## Модель Task

| Поле          | Тип      | Описание                                      |
|---------------|----------|-----------------------------------------------|
| `id`          | int      | Первичный ключ                                |
| `title`       | string   | Заголовок задачи (обязательный)               |
| `description` | string?  | Описание (необязательный)                     |
| `status`      | enum     | `todo` / `in_progress` / `done`               |
| `created_at`  | datetime | Дата создания (генерируется автоматически)    |
| `updated_at`  | datetime | Дата обновления (обновляется автоматически)   |

---

## Остановка

```bash
docker-compose down
```

Чтобы также удалить данные базы:

```bash
docker-compose down -v
```

---

## Технологический стек

- **Python 3.12**
- **FastAPI 0.115**
- **SQLAlchemy 2.0** (async) + **asyncpg**
- **Pydantic v2** + **pydantic-settings**
- **PostgreSQL 15**
- **Docker** / **Docker Compose**
- **Uvicorn**
