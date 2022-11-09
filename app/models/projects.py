from typing import Optional
from enum import Enum

from app.models.core import IDModelMixin, CoreModel


class ProjectBase(CoreModel):
    title: Optional[str]
    description: Optional[str]
    image: Optional[str]


class ProjectCreate(ProjectBase):
    title: str


class ProjectUpdate(ProjectBase):
    pass


class ProjectInDB(IDModelMixin, ProjectBase):
    title: str
    description: str
    image: str


class ProjectPublic(IDModelMixin, ProjectBase):
    pass