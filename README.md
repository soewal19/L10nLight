# L10nLight Microservice

[English](#english) | [Русский](#русский)

---

## Русский

### Описание проекта

L10nLight - это микросервис на Python, построенный с использованием фреймворка Litestar, который реплицирует функциональность существующего Django REST Framework приложения для управления офферволлами и предложениями.

**Основные возможности:**
- Управление офферволлами с уникальными токенами
- Поддержка 34 типов предложений через `OfferChoices`
- API для получения офферволлов и связанных предложений
- Docker-поддержка для продакшн и разработки
- Автоматическая сортировка предложений внутри офферволлов

### Технологический стек

- **Litestar 2.8+** - веб-фреймворк
- **SQLAlchemy 2.0+** - ORM с асинхронной поддержкой
- **Granian** - ASGI сервер
- **PostgreSQL** - основная база данных
- **Pydantic** - валидация данных и схемы
- **Docker** - контейнеризация
- **Nginx** -反向代理 сервер

### Архитектура

Проект следует принципам чистой архитектуры:

```
app/
├── domain/           # Бизнес-сущности и порты
├── application/      # Сервисы бизнес-логики
├── infrastructure/   # Реализация репозиториев
├── routes/          # Контроллеры и эндпоинты
├── schemas.py       # Pydantic схемы
├── models.py        # SQLAlchemy модели
└── server.py        # Конфигурация приложения
```

### API Эндпоинты

- `GET /api/offerwalls/{token}` - Получить офферволл по токену
- `GET /api/offerwalls/by_url/{url}` - Получить офферволл по URL
- `GET /api/offerwalls/get_offer_names` - Получить список названий предложений
- `GET /api/offerwalls` - Получить список офферволлов с фильтрацией и пагинацией

### Как запустить

#### Способ 1: Docker (рекомендуется)

1. **Клонирование репозитория:**
```bash
git clone https://github.com/soewal19/L10nLight
cd l10nlight
```

2. **Запуск через Docker Compose:**
```bash
docker-compose up --build
```

3. **Доступ к сервисам:**
- API: http://localhost:8000
- API через Nginx: http://localhost/api
- OpenAPI документация: http://localhost:8000/schema

#### Способ 2: Локальный запуск

1. **Создание виртуального окружения:**
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/Mac
source .venv/bin/activate
```

2. **Установка зависимостей:**
```bash
pip install -r requirements.txt
```

3. **Настройка переменных окружения:**
```bash
cp .env.example .env
# Отредактируйте .env файл с вашими настройками
```

4. **Запуск PostgreSQL (если не используется Docker):**
```bash
# Убедитесь, что PostgreSQL запущен и доступен
```

5. **Запуск приложения:**
```bash
python -m app.server
```

### Переменные окружения

```bash
# Основные настройки
APP_ENV=development
APP_SERVER_HOST=0.0.0.0
APP_SERVER_PORT=8000
APP_ALLOWED_ORIGINS='["*"]'
APP_GRANIAN_WORKERS=1

# База данных
APP_DB_URL=postgresql+asyncpg://user:password@localhost:5432/dbname

# Логирование
LOG_LEVEL=INFO
ECHO_SQL=false
```

### Тестирование

Подробная информация в [docs/tests/README.md](docs/tests/README.md)

**Быстрый запуск тестов:**
```bash
# Установка зависимостей для тестов
pip install -r requirements.txt

# Запуск тестов
pytest -q

# Запуск с подробным выводом
pytest -v

# Запуск конкретного теста
pytest tests/test_offerwalls.py::test_get_offer_names -v
```

### Разработка

**Линтинг и форматирование:**
```bash
# Форматирование кода
black app/ tests/

# Проверка стиля
black --check app/ tests/
```

**Миграции базы данных:**
Проект использует автоматическое создание таблиц через SQLAlchemy. При изменении моделей:

```bash
# Для разработки с SQLite таблицы создаются автоматически
# Для PostgreSQL используйте Alembic для миграций
```

### Docker для разработки

```bash
# Запуск только базы данных
docker-compose up db -d

# Запуск с горячей перезагрузкой
docker-compose -f docker-compose.dev.yaml up --build
```

---

## English

### Project Description

L10nLight is a Python microservice built with the Litestar framework that replicates the functionality of an existing Django REST Framework application for managing offer walls and associated offers.

**Key Features:**
- Manage offer walls with UUID-based tokens
- Support for 34 offer types via `OfferChoices`
- API endpoints for retrieving offer walls and offers
- Docker support for production and development
- Automatic ordering of offers within offer walls

### Technology Stack

- **Litestar 2.8+** - Web framework
- **SQLAlchemy 2.0+** - ORM with async support
- **Granian** - ASGI server
- **PostgreSQL** - Primary database
- **Pydantic** - Data validation and schemas
- **Docker** - Containerization
- **Nginx** - Reverse proxy server

### Architecture

The project follows clean architecture principles:

```
app/
├── domain/           # Business entities and ports
├── application/      # Business logic services
├── infrastructure/   # Repository implementations
├── routes/          # Controllers and endpoints
├── schemas.py       # Pydantic schemas
├── models.py        # SQLAlchemy models
└── server.py        # Application configuration
```

### API Endpoints

- `GET /api/offerwalls/{token}` - Get offer wall by token
- `GET /api/offerwalls/by_url/{url}` - Get offer wall by URL
- `GET /api/offerwalls/get_offer_names` - Get list of offer names
- `GET /api/offerwalls` - Get offer walls list with filtering and pagination

### How to Run

#### Method 1: Docker (Recommended)

1. **Clone repository:**
```bash
git clone https://github.com/soewal19/L10nLight
cd l10nlight
```

2. **Run with Docker Compose:**
```bash
docker-compose up --build
```

3. **Access services:**
- API: http://localhost:8000
- API via Nginx: http://localhost/api
- OpenAPI docs: http://localhost:8000/schema

#### Method 2: Local Development

1. **Create virtual environment:**
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/Mac
source .venv/bin/activate
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Setup environment variables:**
```bash
cp .env.example .env
# Edit .env file with your settings
```

4. **Start PostgreSQL (if not using Docker):**
```bash
# Make sure PostgreSQL is running and accessible
```

5. **Run application:**
```bash
python -m app.server
```

### Environment Variables

```bash
# Basic settings
APP_ENV=development
APP_SERVER_HOST=0.0.0.0
APP_SERVER_PORT=8000
APP_ALLOWED_ORIGINS='["*"]'
APP_GRANIAN_WORKERS=1

# Database
APP_DB_URL=postgresql+asyncpg://user:password@localhost:5432/dbname

# Logging
LOG_LEVEL=INFO
ECHO_SQL=false
```

### Testing

See [docs/tests/README.md](docs/tests/README.md) for detailed information.

**Quick test run:**
```bash
# Install test dependencies
pip install -r requirements.txt

# Run tests
pytest -q

# Run with verbose output
pytest -v

# Run specific test
pytest tests/test_offerwalls.py::test_get_offer_names -v
```

### Development

**Linting and formatting:**
```bash
# Format code
black app/ tests/

# Check style
black --check app/ tests/
```

**Database migrations:**
The project uses automatic table creation via SQLAlchemy. When changing models:

```bash
# For development with SQLite, tables are created automatically
# For PostgreSQL, use Alembic for migrations
```

### Docker for Development

```bash
# Run only database
docker-compose up db -d

# Run with hot reload
docker-compose -f docker-compose.dev.yaml up --build
```

---

## Дополнительная документация

- **[QUICKSTART.md](QUICKSTART.md)** - Быстрый старт для разработчиков
- **[WORKFLOW.md](WORKFLOW.md)** - Подробный воркфлоу разработки
- **[docs/tests/README.md](docs/tests/README.md)** - Руководство по тестированию
- **[docs/c4/README.md](docs/c4/README.md)** - C4 архитектура

## License

MIT License - see LICENSE file for details.
