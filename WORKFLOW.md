# Development Workflow Guide

[English](#english) | [Русский](#русский)

---

## English

### Overview

This document describes the complete development workflow for the L10nLight microservice project, from setup to deployment.

### Prerequisites

- Python 3.12+
- Docker & Docker Compose
- Git
- PostgreSQL (for local development)
- Make (optional, for convenience)

### Project Structure

```
L10nLight/
├── app/                    # Main application code
│   ├── domain/            # Business logic layer
│   ├── application/       # Service layer
│   ├── infrastructure/    # Data access layer
│   ├── routes/           # API controllers
│   ├── schemas.py        # Pydantic schemas
│   ├── models.py         # SQLAlchemy models
│   └── server.py         # Application entry point
├── tests/                 # Test suite
├── docs/                  # Documentation
├── nginx/                 # Nginx configuration
├── docker-compose.yaml    # Production compose
├── requirements.txt       # Python dependencies
├── pyproject.toml        # Project configuration
└── README.md             # Project overview
```

### Development Workflow

#### 1. Initial Setup

```bash
# Clone repository
git clone https://github.com/soewal19/L10nLight
cd L10nLight

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# or .venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt  # if exists

# Copy environment file
cp .env.example .env
# Edit .env with your configuration
```

#### 2. Local Development

**Option A: Docker (Recommended)**
```bash
# Start all services
docker-compose up --build

# Start only database
docker-compose up db -d

# Start with hot reload (if docker-compose.dev.yaml exists)
docker-compose -f docker-compose.dev.yaml up --build
```

**Option B: Local Python**
```bash
# Start PostgreSQL locally
# Then start the application
python -m app.server
```

#### 3. Database Management

```bash
# Using Docker
docker-compose exec db psql -U app -d app

# Local PostgreSQL
psql -U app -d app

# Reset database (Docker)
docker-compose down -v
docker-compose up db --build

# Run migrations (if using Alembic)
alembic upgrade head
alembic revision --autogenerate -m "description"
```

#### 4. Testing Workflow

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_offerwalls.py

# Run with verbose output
pytest -v

# Run tests in parallel
pytest -n auto

# Debug failing tests
pytest -x --pdb
```

#### 5. Code Quality

```bash
# Format code
black app/ tests/

# Check formatting
black --check app/ tests/

# Type checking (if using mypy)
mypy app/

# Linting (if using ruff/flake8)
ruff check app/
ruff format app/
```

#### 6. Development Features

**Hot Reload:**
- Docker Compose development configuration
- File watching with automatic restart

**Logging:**
```bash
# Development logs
tail -f logs/app.log

# Docker logs
docker-compose logs -f api
docker-compose logs -f db
```

**Database Inspection:**
```bash
# SQLAlchemy echo
ECHO_SQL=true python -m app.server

# Database URL inspection
python -c "from app.config import settings; print(settings.db_url)"
```

### Git Workflow

#### Branch Strategy

```bash
# Main branches
main          # Production-ready code
develop       # Integration branch

# Feature branches
feature/feature-name
bugfix/bug-description
hotfix/urgent-fix
```

#### Commit Convention

```bash
# Format: <type>(<scope>): <description>

feat(api): add offerwall by_url endpoint
fix(db): resolve unique constraint error
docs(readme): update installation instructions
test(offerwalls): add pagination tests
refactor(schemas): extract common fields
```

#### Development Cycle

```bash
# 1. Create feature branch
git checkout -b feature/new-endpoint

# 2. Make changes
# ... code changes ...

# 3. Run tests
pytest

# 4. Format code
black .

# 5. Commit changes
git add .
git commit -m "feat(api): add new endpoint"

# 6. Push and create PR
git push origin feature/new-endpoint
# Create Pull Request on GitHub/GitLab
```

### API Development

#### Adding New Endpoints

1. **Define Schema** (`app/schemas.py`):
```python
class NewEndpointResponse(BaseModel):
    message: str
    data: Optional[dict] = None
```

2. **Update Service** (`app/application/`):
```python
async def new_service_method(self, param: str) -> dict:
    # Business logic here
    return {"result": "success"}
```

3. **Add Repository Method** (`app/infrastructure/`):
```python
async def get_by_custom_field(self, field: str) -> Optional[Entity]:
    # Database query here
    pass
```

4. **Create Controller** (`app/routes/`):
```python
@get("/new-endpoint/{param}")
async def new_endpoint(self, service: OfferWallService, param: str) -> NewEndpointResponse:
    result = await service.new_service_method(param)
    return NewEndpointResponse(message="Success", data=result)
```

5. **Add Tests** (`tests/`):
```python
@pytest.mark.asyncio
async def test_new_endpoint(async_client):
    response = await async_client.get("/api/new-endpoint/test")
    assert response.status_code == 200
    assert response.json()["message"] == "Success"
```

#### Database Changes

```bash
# 1. Update models (app/models.py)
# 2. Generate migration (if using Alembic)
alembic revision --autogenerate -m "Add new field"

# 3. Apply migration
alembic upgrade head

# 4. Update schemas and tests
```

### Environment Configuration

#### Development Environment

```bash
# .env.development
APP_ENV=development
APP_SERVER_HOST=127.0.0.1
APP_SERVER_PORT=8000
APP_DB_URL=postgresql+asyncpg://app:app@localhost:5432/app_dev
APP_ALLOWED_ORIGINS='["http://localhost:3000", "http://localhost:8000"]'
LOG_LEVEL=DEBUG
ECHO_SQL=true
```

#### Test Environment

```bash
# .env.test
APP_ENV=testing
APP_DB_URL=sqlite+aiosqlite:///test.sqlite
APP_ALLOWED_ORIGINS='["*"]'
LOG_LEVEL=WARNING
ECHO_SQL=false
```

#### Production Environment

```bash
# .env.production
APP_ENV=production
APP_SERVER_HOST=0.0.0.0
APP_SERVER_PORT=8000
APP_DB_URL=postgresql+asyncpg://user:pass@db:5432/app_prod
APP_ALLOWED_ORIGINS='["https://yourdomain.com"]'
LOG_LEVEL=INFO
ECHO_SQL=false
```

### Docker Workflow

#### Development Docker

```yaml
# docker-compose.dev.yaml
version: "3.9"
services:
  api:
    build: .
    volumes:
      - ./app:/app/app  # Hot reload
    environment:
      - APP_ENV=development
      - ECHO_SQL=true
    ports:
      - "8000:8000"
```

#### Production Docker

```bash
# Build for production
docker build -t l10nlight:latest .

# Tag and push
docker tag l10nlight:latest registry.com/l10nlight:v1.0.0
docker push registry.com/l10nlight:v1.0.0

# Run production container
docker run -d \
  --name l10nlight \
  -p 8000:8000 \
  --env-file .env.production \
  registry.com/l10nlight:v1.0.0
```

### Monitoring and Debugging

#### Health Checks

```bash
# Application health
curl http://localhost:8000/health

# Database health
docker-compose exec db pg_isready -U app

# Docker health
docker-compose ps
```

#### Debugging

```bash
# Python debugger
python -m pdb -m app.server

# Docker debugging
docker-compose exec api bash
docker-compose logs -f api

# Performance profiling
python -m cProfile -o profile.stats -m app.server
```

#### Monitoring

```bash
# Application metrics
curl http://localhost:8000/metrics

# Resource usage
docker stats

# Database queries
# Enable ECHO_SQL=true in development
```

### Deployment Workflow

#### Pre-deployment Checklist

```bash
# 1. Run full test suite
pytest --cov=app

# 2. Code quality checks
black --check .
ruff check .

# 3. Security scan (if using bandit)
bandit -r app/

# 4. Dependency check (if using safety)
safety check

# 5. Build Docker image
docker build -t l10nlight:test .
```

#### Deployment Steps

```bash
# 1. Build production image
docker build -t l10nlight:latest .

# 2. Deploy to staging
docker-compose -f docker-compose.staging.yaml up -d

# 3. Run smoke tests
pytest tests/smoke/

# 4. Deploy to production
docker-compose up -d

# 5. Verify deployment
curl https://yourdomain.com/api/offerwalls/get_offer_names
```

### Troubleshooting

#### Common Issues

**Database Connection Errors:**
```bash
# Check PostgreSQL status
docker-compose exec db pg_isready

# Verify connection string
python -c "from app.config import settings; print(settings.db_url)"

# Reset database
docker-compose down -v
docker-compose up db
```

**Import Errors:**
```bash
# Check Python path
python -c "import sys; print(sys.path)"

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

**Docker Issues:**
```bash
# Clear Docker cache
docker system prune -a

# Rebuild containers
docker-compose build --no-cache

# Check logs
docker-compose logs api
```

#### Performance Issues

```bash
# Profile application
python -m cProfile -o profile.stats -m app.server

# Check database queries
ECHO_SQL=true python -m app.server

# Monitor resources
docker stats
```

---

## Русский

### Обзор

Этот документ описывает полный цикл разработки микросервиса L10nLight, от настройки до развертывания.

### Предварительные требования

- Python 3.12+
- Docker & Docker Compose
- Git
- PostgreSQL (для локальной разработки)
- Make (опционально, для удобства)

### Структура проекта

```
L10nLight/
├── app/                    # Основной код приложения
│   ├── domain/            # Слой бизнес-логики
│   ├── application/       # Сервисный слой
│   ├── infrastructure/    # Слой доступа к данным
│   ├── routes/           # API контроллеры
│   ├── schemas.py        # Pydantic схемы
│   ├── models.py         # SQLAlchemy модели
│   └── server.py         # Точка входа приложения
├── tests/                 # Набор тестов
├── docs/                  # Документация
├── nginx/                 # Конфигурация Nginx
├── docker-compose.yaml    # Production compose
├── requirements.txt       # Python зависимости
├── pyproject.toml        # Конфигурация проекта
└── README.md             # Обзор проекта
```

### Воркфлоу разработки

#### 1. Начальная настройка

```bash
# Клонирование репозитория
git clone <repository-url>
cd L10nLight

# Создание виртуального окружения
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# или .venv\Scripts\activate  # Windows

# Установка зависимостей
pip install -r requirements.txt
pip install -r requirements-dev.txt  # если существует

# Копирование файла окружения
cp .env.example .env
# Отредактируйте .env с вашей конфигурацией
```

#### 2. Локальная разработка

**Вариант А: Docker (рекомендуется)**
```bash
# Запуск всех сервисов
docker-compose up --build

# Запуск только базы данных
docker-compose up db -d

# Запуск с горячей перезагрузкой (если есть docker-compose.dev.yaml)
docker-compose -f docker-compose.dev.yaml up --build
```

**Вариант Б: Локальный Python**
```bash
# Запуск PostgreSQL локально
# Затем запуск приложения
python -m app.server
```

#### 3. Управление базой данных

```bash
# Используя Docker
docker-compose exec db psql -U app -d app

# Локальный PostgreSQL
psql -U app -d app

# Сброс базы данных (Docker)
docker-compose down -v
docker-compose up db --build

# Запуск миграций (если используется Alembic)
alembic upgrade head
alembic revision --autogenerate -m "описание"
```

#### 4. Тестирование

```bash
# Запуск всех тестов
pytest

# Запуск с покрытием кода
pytest --cov=app --cov-report=html

# Запуск конкретного файла тестов
pytest tests/test_offerwalls.py

# Запуск с подробным выводом
pytest -v

# Параллельный запуск тестов
pytest -n auto

# Отладка падающих тестов
pytest -x --pdb
```

#### 5. Качество кода

```bash
# Форматирование кода
black app/ tests/

# Проверка форматирования
black --check app/ tests/

# Проверка типов (если используется mypy)
mypy app/

# Линтинг (если используется ruff/flake8)
ruff check app/
ruff format app/
```

#### 6. Возможности разработки

**Горячая перезагрузка:**
- Docker Compose конфигурация для разработки
- Отслеживание файлов с автоматическим перезапуском

**Логирование:**
```bash
# Логи разработки
tail -f logs/app.log

# Docker логи
docker-compose logs -f api
docker-compose logs -f db
```

**Инспекция базы данных:**
```bash
# SQLAlchemy echo
ECHO_SQL=true python -m app.server

# Проверка URL базы данных
python -c "from app.config import settings; print(settings.db_url)"
```

### Git воркфлоу

#### Стратегия веток

```bash
# Основные ветки
main          # Код для продакшена
develop       # Ветка интеграции

# Ветки функций
feature/название-функции
bugfix/описание-бага
hotfix/срочное-исправление
```

#### Конвенция коммитов

```bash
# Формат: <тип>(<область>): <описание>

feat(api): добавить эндпоинт by_url для офферволлов
fix(db): исправить ошибку уникального ограничения
docs(readme): обновить инструкции установки
test(offerwalls): добавить тесты пагинации
refactor(schemas): извлечь общие поля
```

#### Цикл разработки

```bash
# 1. Создание ветки функции
git checkout -b feature/new-endpoint

# 2. Внесение изменений
# ... изменения кода ...

# 3. Запуск тестов
pytest

# 4. Форматирование кода
black .

# 5. Коммит изменений
git add .
git commit -m "feat(api): добавить новый эндпоинт"

# 6. Пуш и создание PR
git push origin feature/new-endpoint
# Создание Pull Request на GitHub/GitLab
```

### Разработка API

#### Добавление новых эндпоинтов

1. **Определение схемы** (`app/schemas.py`):
```python
class NewEndpointResponse(BaseModel):
    message: str
    data: Optional[dict] = None
```

2. **Обновление сервиса** (`app/application/`):
```python
async def new_service_method(self, param: str) -> dict:
    # Бизнес-логика здесь
    return {"result": "success"}
```

3. **Добавление метода репозитория** (`app/infrastructure/`):
```python
async def get_by_custom_field(self, field: str) -> Optional[Entity]:
    # Запрос к базе данных здесь
    pass
```

4. **Создание контроллера** (`app/routes/`):
```python
@get("/new-endpoint/{param}")
async def new_endpoint(self, service: OfferWallService, param: str) -> NewEndpointResponse:
    result = await service.new_service_method(param)
    return NewEndpointResponse(message="Success", data=result)
```

5. **Добавление тестов** (`tests/`):
```python
@pytest.mark.asyncio
async def test_new_endpoint(async_client):
    response = await async_client.get("/api/new-endpoint/test")
    assert response.status_code == 200
    assert response.json()["message"] == "Success"
```

#### Изменения в базе данных

```bash
# 1. Обновление моделей (app/models.py)
# 2. Генерация миграции (если используется Alembic)
alembic revision --autogenerate -m "Добавление нового поля"

# 3. Применение миграции
alembic upgrade head

# 4. Обновление схем и тестов
```

### Конфигурация окружения

#### Окружение разработки

```bash
# .env.development
APP_ENV=development
APP_SERVER_HOST=127.0.0.1
APP_SERVER_PORT=8000
APP_DB_URL=postgresql+asyncpg://app:app@localhost:5432/app_dev
APP_ALLOWED_ORIGINS='["http://localhost:3000", "http://localhost:8000"]'
LOG_LEVEL=DEBUG
ECHO_SQL=true
```

#### Тестовое окружение

```bash
# .env.test
APP_ENV=testing
APP_DB_URL=sqlite+aiosqlite:///test.sqlite
APP_ALLOWED_ORIGINS='["*"]'
LOG_LEVEL=WARNING
ECHO_SQL=false
```

#### Продакшн окружение

```bash
# .env.production
APP_ENV=production
APP_SERVER_HOST=0.0.0.0
APP_SERVER_PORT=8000
APP_DB_URL=postgresql+asyncpg://user:pass@db:5432/app_prod
APP_ALLOWED_ORIGINS='["https://yourdomain.com"]'
LOG_LEVEL=INFO
ECHO_SQL=false
```

### Docker воркфлоу

#### Docker для разработки

```yaml
# docker-compose.dev.yaml
version: "3.9"
services:
  api:
    build: .
    volumes:
      - ./app:/app/app  # Горячая перезагрузка
    environment:
      - APP_ENV=development
      - ECHO_SQL=true
    ports:
      - "8000:8000"
```

#### Docker для продакшена

```bash
# Сборка для продакшена
docker build -t l10nlight:latest .

# Тегирование и пуш
docker tag l10nlight:latest registry.com/l10nlight:v1.0.0
docker push registry.com/l10nlight:v1.0.0

# Запуск продакшн контейнера
docker run -d \
  --name l10nlight \
  -p 8000:8000 \
  --env-file .env.production \
  registry.com/l10nlight:v1.0.0
```

### Мониторинг и отладка

#### Проверки работоспособности

```bash
# Работоспособность приложения
curl http://localhost:8000/health

# Работоспособность базы данных
docker-compose exec db pg_isready -U app

# Работоспособность Docker
docker-compose ps
```

#### Отладка

```bash
# Python отладчик
python -m pdb -m app.server

# Отладка в Docker
docker-compose exec api bash
docker-compose logs -f api

# Профилирование производительности
python -m cProfile -o profile.stats -m app.server
```

#### Мониторинг

```bash
# Метрики приложения
curl http://localhost:8000/metrics

# Использование ресурсов
docker stats

# Запросы к базе данных
# Включите ECHO_SQL=true в разработке
```

### Воркфлоу развертывания

#### Чек-лист перед развертыванием

```bash
# 1. Запуск полного набора тестов
pytest --cov=app

# 2. Проверки качества кода
black --check .
ruff check .

# 3. Проверка безопасности (если используется bandit)
bandit -r app/

# 4. Проверка зависимостей (если используется safety)
safety check

# 5. Сборка Docker образа
docker build -t l10nlight:test .
```

#### Шаги развертывания

```bash
# 1. Сборка продакшн образа
docker build -t l10nlight:latest .

# 2. Развертывание на стейджинг
docker-compose -f docker-compose.staging.yaml up -d

# 3. Запуск smoke тестов
pytest tests/smoke/

# 4. Развертывание на продакшн
docker-compose up -d

# 5. Проверка развертывания
curl https://yourdomain.com/api/offerwalls/get_offer_names
```

### Устранение проблем

#### Распространенные проблемы

**Ошибки подключения к базе данных:**
```bash
# Проверка статуса PostgreSQL
docker-compose exec db pg_isready

# Проверка строки подключения
python -c "from app.config import settings; print(settings.db_url)"

# Сброс базы данных
docker-compose down -v
docker-compose up db
```

**Ошибки импорта:**
```bash
# Проверка Python пути
python -c "import sys; print(sys.path)"

# Переустановка зависимостей
pip install -r requirements.txt --force-reinstall
```

**Проблемы с Docker:**
```bash
# Очистка Docker кеша
docker system prune -a

# Пересборка контейнеров
docker-compose build --no-cache

# Проверка логов
docker-compose logs api
```

#### Проблемы производительностью

```bash
# Профилирование приложения
python -m cProfile -o profile.stats -m app.server

# Проверка запросов к базе данных
ECHO_SQL=true python -m app.server

# Мониторинг ресурсов
docker stats
```

---

## Дополнительные ресурсы

### Документация
- [Litestar Documentation](https://docs.litestar.dev/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [Docker Documentation](https://docs.docker.com/)

### Инструменты
- [Black Code Formatter](https://black.readthedocs.io/)
- [Ruff Linter](https://docs.astral.sh/ruff/)
- [Pytest Testing Framework](https://docs.pytest.org/)
- [Alembic Database Migrations](https://alembic.sqlalchemy.org/)

### Лучшие практики
- [Clean Architecture](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
- [Python Development Guidelines](https://peps.python.org/pep-0008/)
- [API Design Guidelines](https://restfulapi.net/)
