from app.db.repositories.base import BaseRepository
from app.models.projects import ProjectCreate, ProjectUpdate, ProjectInDB


CREATE_PROJECT_QUERY = """
    INSERT INTO projects (title, description, image)
    VALUES (:title, :description, :image)
    RETURNING id, title, description, image;
"""


class ProjectsRepository(BaseRepository):
    
    async def create_project(self, *, new_project: ProjectCreate) -> ProjectInDB:
        query_values = new_project.dict()
        project = await self.db.fetch_one(
            query=CREATE_PROJECT_QUERY, values=query_values
        )

        return ProjectInDB(**project)