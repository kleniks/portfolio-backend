import pytest
import pytest_asyncio

from httpx import AsyncClient
from fastapi import FastAPI

from starlette.status import HTTP_200_OK, \
                             HTTP_201_CREATED,\
                             HTTP_404_NOT_FOUND, \
                             HTTP_422_UNPROCESSABLE_ENTITY
                             

from app.models.projects import ProjectCreate, ProjectInDB


pytestmark = pytest.mark.asyncio


@pytest_asyncio.fixture
def new_project():
    return ProjectCreate(
        title="test project",
        description="test description",
        image="test.jpg",
    )


class TestProjectsRoutes:
    async def test_routes_exit(self, app: FastAPI, client: AsyncClient) -> None:
        res = await client.post(app.url_path_for("projects:create-project"), json={})
        assert res.status_code != HTTP_404_NOT_FOUND

    async def test_invalid_input_raises_error(
        self, app: FastAPI, client: AsyncClient
    ) -> None:
        res = await client.post(app.url_path_for("projects:create-project"), json={})
        assert res.status_code == HTTP_422_UNPROCESSABLE_ENTITY


class TestCreateProject:
    """Тестирование создания записи проекта"""

    async def test_valid_input_creates_project(
        self, app: FastAPI, client: AsyncClient, new_project: ProjectCreate
    ) -> None:
        res = await client.post(
            app.url_path_for("projects:create-project"),
            json={"new_project": new_project.dict()}
        )
        assert res.status_code == HTTP_201_CREATED
        created_project = ProjectCreate(**res.json())
        assert created_project == new_project

    @pytest.mark.parametrize(
        "invalid_payload, status_code",
        (
            (None, 422),
            ({}, 422),
            ({"title": "test_name"}, 422),
            ({"image": "test.jpg"}, 422),
            ({"title": "test_name", "description": "test"}, 422),
        ),
    )
    async def test_invalid_input_raises_error(
        self, app: FastAPI, client: AsyncClient,
        invalid_payload: dict, status_code: int
    ) -> None:
        res = await client.post(
            app.url_path_for("projects:create-project"),
            json={"new_project": invalid_payload},
        )
        assert res.status_code == status_code


class TestGetProjetc:
    async def test_get_project_by_id(self, app: FastAPI, client: AsyncClient) -> None:
        res = await client.get(
            app.url_path_for("projects:get-project-by-id", id=1)
        )
        assert res.status_code == HTTP_200_OK
        project = ProjectInDB(**res.json())
        assert project.id == 1