# Task Manager API & UI (Этап 2)

REST API для управления задачами, построенный на **FastAPI** + **PostgreSQL**, с поддержкой **JWT-аутентификации**, привязкой задач к пользователям и минималистичным **Vanilla JS Frontend**. 

Поддерживает регистрацию, вход, создание, просмотр, обновление и удаление задач. Пользователи могут управлять только своими собственными задачами.

---

## Структура проекта

```
TestTaskManager/
├── app/
│   ├── __init__.py
│   ├── auth.py          # Логика JWT, хэширование (bcrypt) и зависимости
│   ├── config.py        # Настройки приложения (pydantic-settings)
│   ├── database.py      # Async SQLAlchemy движок и сессии
│   ├── models.py        # ORM-модели (User, Task)
│   ├── schemas.py       # Pydantic-схемы (Auth, User, Task)
│   ├── main.py          # Точка входа FastAPI, подключение роутеров
│   └── routers/
│       ├── __init__.py
│       ├── auth.py      # Эндпоинты /auth (register, login)
│       └── tasks.py     # Эндпоинты /tasks (protected)
├── static/
│   └── index.html       # Frontend с поддержкой авторизации
├── .env
├── .gitignore
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── README.md
```

---

## Быстрый старт

### 1. Настройте `.env`

Создайте файл `.env` в корне проекта (можно скопировать из `.env.example`):

```env
DATABASE_URL=postgresql+asyncpg://taskuser:taskpassword@db:5432/taskdb
SECRET_KEY=your_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 2. Запустите через Docker Compose

```bash
docker compose up --build -d
```

Команда соберет образ и запустит:
- **db**: PostgreSQL 15.
- **api**: FastAPI приложение.

### 3. Откройте Frontend UI

Перейдите по адресу:
```
http://localhost:8000/
```

Интерфейс позволяет:
- **Зарегистрироваться** и **Войти**.
- Управлять списком **своих** задач.
- Фильтровать по статусу и сортировать по дате.

---

## API Эндпоинты

### Аутентификация (`/auth`)
| Метод  | URL               | Описание                          |
|--------|-------------------|-----------------------------------|
| `POST` | `/auth/register`  | Регистрация нового пользователя   |
| `POST` | `/auth/login`     | Вход и получение JWT-токена       |

### Задачи (`/tasks`) — Требуют `Authorization: Bearer <token>`
| Метод    | URL                  | Описание                                  |
|----------|----------------------|-------------------------------------------|
| `POST`   | `/tasks/`            | Создать задачу (автопривязка к юзеру)     |
| `GET`    | `/tasks/`            | Список задач текущего пользователя        |
| `GET`    | `/tasks/{task_id}`   | Получить свою задачу по ID                |
| `PATCH`  | `/tasks/{task_id}`   | Частичное обновление своей задачи         |
| `DELETE` | `/tasks/{task_id}`   | Удалить свою задачу                       |

---

## Технические особенности

- **Безопасность**: Пароли хэшируются с использованием `bcrypt`. JWT токены используются для авторизации.
- **Валидация**: Строгая проверка входных данных через Pydantic (например, `title` не может быть пустым).
- **База данных**: Асинхронная работа с PostgreSQL через SQLAlchemy 2.0.
- **Автоматизация**: Поля `created_at` и `updated_at` управляются на уровне БД/ORM.

---

## Остановка и очистка

Остановка:
```bash
docker compose down
```

Остановка с полным удалением данных базы:
```bash
docker compose down -v
```

---

## Технологический стек

- **Backend**: Python 3.12, FastAPI, SQLAlchemy (Async), PostgreSQL, JWT (jose), Bcrypt.
- **Frontend**: HTML5, CSS3, Vanilla JS (Fetch API).
- **Инфраструктура**: Docker, Docker Compose.
