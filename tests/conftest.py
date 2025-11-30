pytest_plugins = ("pytest_asyncio",)

import os
import pytest
import pytest_asyncio
from litestar import Litestar
from httpx import AsyncClient, ASGITransport

# Set test-specific env BEFORE importing config/server
os.environ.setdefault("APP_ENV", "test")
os.environ.setdefault("APP_SERVER_HOST", "127.0.0.1")
os.environ.setdefault("APP_SERVER_PORT", "8000")
os.environ.setdefault("APP_ALLOWED_ORIGINS", '["*"]')
os.environ.setdefault("APP_DB_URL", "sqlite+aiosqlite:///./test.sqlite")
os.environ.setdefault("APP_GRANIAN_WORKERS", "1")

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.server import app as litestar_app  # noqa: E402
from app.db import init_db, SessionLocal  # noqa: E402

@pytest.fixture(scope="session", autouse=True)
def setup_db():
    # initialize tables once for sqlite
    import asyncio
    asyncio.run(init_db())

@pytest.fixture
def app() -> Litestar:
    return litestar_app

# Фикстура клиента: используем ASGITransport вместо устаревшего параметра app
@pytest_asyncio.fixture
async def client(app: Litestar):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac