from typing import List

from fastapi import APIRouter, Body, Depends
from starlette.status import HTTP_201_CREATED

from app.models.projects import ProjectCreate, ProjectPublic
from app.db.repositories.projects import ProjectsRepository
from app.api.dependecies.database import get_repository

router = APIRouter()


@router.get('/')
async def get_all_projects() -> List[dict]:
    projects = [
        {'id': 1, 'project_name': 'some project', 'description': 'this is projects'},
        {'id': 2, 'project_name': 'anpother project', 'description': 'that is projects'},
    ]

    return projects


@router.post(
    "/", 
    response_model=ProjectPublic, 
    name="projects:create-project",
    status_code=HTTP_201_CREATED,
    )
async def create_new_project(
    new_project: ProjectCreate = Body(...,embed=True),
    projects_repo: ProjectsRepository = Depends(get_repository(ProjectsRepository)),
) -> ProjectPublic:
    created_project = await projects_repo.create_project(new_project=new_project)

    return created_project
    