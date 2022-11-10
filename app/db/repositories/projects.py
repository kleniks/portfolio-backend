from app.db.repositories.base import BaseRepository
from app.models.projects import ProjectCreate, ProjectUpdate, ProjectInDB


CREATE_PROJECT_QUERY = """
    INSERT INTO projects (title, description, image)
    VALUES (:title, :description, :image)
    RETURNING id, title, description, image;
"""
GET_PROJECT_BY_ID_QUERY = """
    SELECT id, title, description, image
    FROM projects
    WHERE id = :id;
"""


class ProjectsRepository(BaseRepository):
    
    async def create_project(self, *, new_project: ProjectCreate) -> ProjectInDB:
        query_values = new_project.dict()
        project = await self.db.fetch_one(
            query=CREATE_PROJECT_QUERY, values=query_values
        )

        return ProjectInDB(**project)

    async def get_project_by_id(self, *, id: int) -> ProjectInDB:
        project = await self.db.fetch_one(query=GET_PROJECT_BY_ID_QUERY, values={"id": id})

        if not project:
            return None

        return ProjectInDB(**project)