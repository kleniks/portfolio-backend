from typing import List

from fastapi import APIRouter, Body, Depends, HTTPException
from starlette.status import HTTP_201_CREATED, \
                             HTTP_404_NOT_FOUND, \
                             HTTP_422_UNPROCESSABLE_ENTITY

from app.models.projects import ProjectCreate, ProjectPublic
from app.db.repositories.projects import ProjectsRepository
from app.api.dependecies.database import get_repository

router = APIRouter()


@router.get("/{id}/", response_model=ProjectPublic, name="projects:get-project-by-id")
async def get_project_by_id(id: int, project_repo: ProjectsRepository = Depends(get_repository(ProjectsRepository))) -> ProjectPublic:
    project = await project_repo.get_project_by_id(id=id)
    if not project:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND, detail="No project found with that id. "
        )

    return project


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
    try:
        created_project = await projects_repo.create_project(new_project=new_project)
    except:
        raise HTTPException(status_code=HTTP_422_UNPROCESSABLE_ENTITY)
    return created_project
    