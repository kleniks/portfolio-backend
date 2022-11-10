import warnings
import os

import pytest
import pytest_asyncio
from asgi_lifespan import LifespanManager

from fastapi import FastAPI
from httpx import AsyncClient
from databases import Database

import alembic
from alembic.config import Config

from app.models.projects import ProjectCreate, ProjectInDB
from app.db.repositories.projects import ProjectsRepository 


# Apply migrations at beginning and end of testing session
@pytest.fixture(scope="session")
def apply_migrations():
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    os.environ["TESTING"] = "1"
    config = Config("alembic.ini")

    alembic.command.upgrade(config, "head")
    yield
    alembic.command.downgrade(config, "base")


# Create a new application for testing
@pytest.fixture
def app(apply_migrations: None) -> FastAPI:
    from app.api.server import get_application

    return  get_application()


# Grab a reference to our database when needed
@pytest_asyncio.fixture
def db(app: FastAPI) -> Database:
    return app.state._db


# Make requests in our tests
@pytest_asyncio.fixture
async def client(app: FastAPI) -> AsyncClient:
    async with LifespanManager(app):
        async with AsyncClient(
            app=app,
            base_url="http://testserver",
            headers={"Content-Type": "application/json"}
        ) as client:
            yield client


@pytest.fixture
async def test_project(db: Database) -> ProjectInDB:
    project_repo = ProjectsRepository(db)
    new_project = ProjectCreate(
        title="fake project title",
        description="fake project description",
        image="fake_image.jpg"
    )

    return await project_repo.create_project(new_project=new_project)