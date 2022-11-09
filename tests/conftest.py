import warnings
import os

import pytest
from asgi_lifespan import LifespanManager

from fastapi import FastAPI
from httpx import AsyncClient
from databases import Database

import alembic
from alembic.config import Config


# Применяем миграции в начале и в конце тестирования. Upgrade и Downgrade соответственно.
@pytest.fixture(scope="session")
def apply_migrations():
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    os.environ["TESTING"] = 1
    config = Config("alembic.ini")

    alembic.command.upgrade(config, "head")
    yield
    alembic.command.downgrade(config, "base")


# Создаем новый экземпляр приложения для тестов
@pytest.fixture
def app(apply_migrations: None) -> FastAPI:
    from app.api.server import get_appliction

    return get_appliction()


# Ссылка на DB
@pytest.fixture
async def db(app: FastAPI) -> Database:
    return app.state._db


# Создаем запросы 
@pytest.fixture
async def client(app: FastAPI) -> AsyncClient:
    async with AsyncClient(
        app=app,
        base_url="http://testserver",
        headers={"Content-Type": "application/json"}
    ) as client:
        yield client





