# Quick Start Guide

## Быстрый старт для разработчиков

### 1. Клонирование и установка
```bash
git clone https://github.com/soewal19/L10nLight
cd L10nLight
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# или .venv\Scripts\activate  # Windows
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### 2. Настройка окружения
```bash
cp .env.example .env
# Отредактируйте .env файл
```

### 3. Запуск
```bash
# Вариант 1: Docker (рекомендуется)
docker-compose up --build

# Вариант 2: Локально
python -m app.server
```

### 4. Проверка работы
```bash
# Проверка API
curl http://localhost:8000/api/offerwalls/get_offer_names

# Запуск тестов
pytest -v
```

---

## Quick Start for Developers

### 1. Clone and install
```bash
git clone <repository-url>
cd L10nLight
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# or .venv\Scripts\activate  # Windows
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### 2. Environment setup
```bash
cp .env.example .env
# Edit .env file
```

### 3. Run
```bash
# Option 1: Docker (recommended)
docker-compose up --build

# Option 2: Local
python -m app.server
```

### 4. Verify
```bash
# Check API
curl http://localhost:8000/api/offerwalls/get_offer_names

# Run tests
pytest -v
```

---

## Полезные команды / Useful Commands

### Разработка / Development
```bash
make dev          # Запуск сервера разработки
make test         # Запуск тестов
make lint         # Проверка кода
make format       # Форматирование кода
make clean        # Очистка кеша
```

### Docker / Docker
```bash
make docker-up    # Запуск Docker сервисов
make docker-down  # Остановка Docker сервисов
make docker-logs  # Просмотр логов
make shell        # Shell в контейнере
```

### Тестирование / Testing
```bash
pytest -v                    # Подробный вывод
pytest --cov=app            # С покрытием кода
pytest -k "offer_names"      # Фильтрация тестов
pytest -x --pdb             # Отладка падающих тестов
```

---

## Следующие шаги / Next Steps

1. Прочитайте [WORKFLOW.md](WORKFLOW.md) для полного понимания процесса разработки
2. Изучите [docs/tests/README.md](docs/tests/README.md) для тестирования
3. Проверьте [docs/c4/README.md](docs/c4/README.md) для архитектуры
4. Изучите API документацию: http://localhost:8000/schema

---

## Получение помощи / Getting Help

- Документация: [README.md](README.md)
- Воркфлоу: [WORKFLOW.md](WORKFLOW.md)
- Тесты: [docs/tests/README.md](docs/tests/README.md)
- Архитектура: [docs/c4/README.md](docs/c4/README.md)
- OpenAPI: http://localhost:8000/schema
