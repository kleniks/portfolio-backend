import pytest

from httpx import AsyncClient
from fastapi import FastAPI

from starlette.status import HTTP_404_NOT_FOUND, HTTP_422_UNPROCESSABLE_ENTITY

pytestmark = pytest.mark.asyncio

class TestProjectsRoutes:
    """Test projects route"""

    async def test_toutes_exit(self, app: FastAPI, client: AsyncClient) -> None:
        res = await client.get(app.url_path_for("projects:get-all-projects"))
        assert res.status_code != HTTP_404_NOT_FOUND
