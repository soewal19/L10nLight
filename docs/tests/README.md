# Тестирование микросервиса L10nLight

## Обзор

Тестовый пакет обеспечивает проверку функциональности API эндпоинтов микросервиса. Тесты используют pytest с асинхронной поддержкой и SQLite базу данных для изолированного тестирования.

## Структура тестов

### Основные файлы:
- `tests/conftest.py` - настройки окружения, фикстуры `app`, `client`, `db_session`
- `tests/test_offerwalls.py` - основные тесты API эндпоинтов
- `tests/unit/` - модульные тесты для отдельных компонентов

### Тестируемые эндпоинты:

#### 1. `GET /api/offerwalls/get_offer_names`
- **Цель**: Проверка соответствия DRF формату
- **Проверки**: 
  - Статус код 200
  - Соответствие списка имен `OfferChoices.choices`
  - Корректная структура JSON ответа

#### 2. `GET /api/offerwalls/{token}`
- **Цель**: Проверка получения офферволла по токену
- **Тест-кейсы**:
  - `test_get_offerwall_not_found` - проверка 404 для несуществующего токена
  - `test_get_offerwall_ok` - проверка успешного ответа с вложенными предложениями
- **Проверки**:
  - Корректность структуры ответа
  - Наличие `offer_assignments` и `popup_assignments`
  - Сортировка предложений по полю `order`

#### 3. `GET /api/offerwalls/by_url/{url}`
- **Цель**: Проверка получения офферволла по URL
- **Тест-кейсы**:
  - `test_get_offerwall_by_url_not_found` - проверка 404 для несуществующего URL
  - `test_get_offerwall_by_url_ok` - проверка успешного ответа

#### 4. `GET /api/offerwalls`
- **Цель**: Проверка списка офферволлов с фильтрацией и пагинацией
- **Тест-кейсы**:
  - `test_list_offerwalls_empty` - пустой список
  - `test_list_offerwalls_with_data` - список с данными
  - `test_list_offerwalls_filtering` - фильтрация по name и url
  - `test_list_offerwalls_pagination` - пагинация

## Подготовка к запуску

### 1. Установка зависимостей

```bash
# Активация виртуального окружения
.venv\Scripts\activate  # Windows
# или
source .venv/bin/activate  # Linux/Mac

# Установка зависимостей
pip install -r requirements.txt
```

### 2. Переменные окружения для тестов

Тесты используют следующие переменные (можно установить в `.env.test`):
```bash
APP_ENV=testing
APP_DB_URL=sqlite+aiosqlite:///test.sqlite
APP_ALLOWED_ORIGINS='["*"]'
LOG_LEVEL=WARNING
ECHO_SQL=false
```

## Запуск тестов

### Базовые команды

```bash
# Запуск всех тестов
pytest

# Запуск с кратким выводом
pytest -q

# Запуск с подробным выводом
pytest -v

# Запуск с покрытием кода
pytest --cov=app --cov-report=html

# Запуск только определенного файла
pytest tests/test_offerwalls.py

# Запуск конкретного теста
pytest tests/test_offerwalls.py::test_get_offer_names -v
```

### Фильтрация тестов

```bash
# Запуск тестов по ключевому слову
pytest -k "offer_names"

# Запуск только успешных тестов
pytest -k "not_found"

# Запуск тестов определенной категории
pytest -m "unit"  # если используются маркеры
```

## Архитектура тестов

### Фикстуры (conftest.py)

#### `async_client`
- Создает асинхронный тестовый клиент Litestar
- Настраивает тестовую базу данных
- Применяет миграции перед каждым тестом

#### `db_session`
- Предоставляет асинхронную сессию базы данных
- Автоматически откатывает изменения после теста
- Использует транзакции для изоляции

#### `sample_data`
- Создает тестовые данные (OfferWall, Offer, Assignment)
- Используется в параметризованных тестах

### Очистка данных

Тесты используют автоматическую очистку:
- **Транзакционный rollback** - изменения откатываются после каждого теста
- **Drop/Create schema** - полная очистка базы данных
- **SQLite файл** - `test.sqlite` пересоздается при необходимости

## Написание новых тестов

### Структура теста

```python
import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_new_endpoint(async_client: AsyncClient):
    # Arrange - подготовка данных
    # Act - выполнение запроса
    response = await async_client.get("/api/new-endpoint")
    
    # Assert - проверка результатов
    assert response.status_code == 200
    assert response.json() == {"key": "value"}
```

### Лучшие практики

1. **Используйте описательные имена тестов**
2. **Следуйте паттерну Arrange-Act-Assert**
3. **Тестируйте как успешные, так и ошибочные сценарии**
4. **Используйте фикстуры для повторяющегося кода**
5. **Проверяйте статус коды и структуру ответа**

### Параметризация

```python
@pytest.mark.parametrize("token,expected_status", [
    ("valid-token", 200),
    ("invalid-token", 404),
    ("", 422),
])
async def test_get_offerwall_various_tokens(async_client, token, expected_status):
    response = await async_client.get(f"/api/offerwalls/{token}")
    assert response.status_code == expected_status
```

## Отладка тестов

### Вывод отладочной информации

```bash
# Показать вывод print() в тестах
pytest -s

# Остановиться на первом падении
pytest -x

# Войти в pdb при падении
pytest --pdb

# Подробный лог SQLAlchemy
pytest -v --log-cli-level=DEBUG
```

### Анализ покрытия

```bash
# Генерация HTML отчета о покрытии
pytest --cov=app --cov-report=html

# Покрытие в терминале
pytest --cov=app --cov-report=term-missing

# Минимальный порог покрытия
pytest --cov=app --cov-fail-under=80
```

## CI/CD интеграция

### GitHub Actions пример

```yaml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: "3.12"
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Run tests
        run: pytest --cov=app --cov-report=xml
      - name: Upload coverage
        uses: codecov/codecov-action@v1
```

## Производительность тестов

### Оптимизация

1. **Используйте `scope='session'` для дорогих фикстур**
2. **Параллельный запуск**: `pytest -n auto`
3. **Кэширование результатов** для медленных операций
4. **Моки** для внешних зависимостей

### Замер времени

```bash
# Показать время выполнения каждого теста
pytest --durations=10

# Профилирование медленных тестов
pytest --profile
```

## Решение проблем

### Распространенные ошибки

1. **`UNIQUE constraint failed`**
   - Причина: Остаточные данные в тестовой БД
   - Решение: Очистка `test.sqlite` или использование транзакций

2. **`asyncio` ошибки**
   - Причина: Смешение sync/async кода
   - Решение: Используйте `@pytest.mark.asyncio`

3. **Timeout ошибки**
   - Причина: Медленные операции с БД
   - Решение: Увеличьте таймаут или оптимизируйте запросы

### Полезные команды

```bash
# Пересоздать тестовую БД
rm test.sqlite && pytest

# Запуск с отладочными логами
pytest -v --log-cli-level=DEBUG

# Проверка синтаксиса тестов
pytest --collect-only
```

## Дополнительные ресурсы

- [Pytest Documentation](https://docs.pytest.org/)
- [Litestar Testing Guide](https://docs.litestar.dev/latest/testing/testing.html)
- [SQLAlchemy Testing Patterns](https://docs.sqlalchemy.org/en/20/orm/session_basics.html#session-faq-whentocreate)