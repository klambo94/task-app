from pydantic import BaseModel
from datetime import datetime
from app.models.enums import IterationType
from app.lib.pagination import CursorPage


class IterationBase(BaseModel):
    title: str
    type: IterationType = IterationType.SPRINT
    description: str | None = None
    goal: str | None = None
    startDate: datetime | None = None
    endDate: datetime | None = None


class IterationCreate(IterationBase):
    spaceId: str
    statusId: str


class IterationUpdate(BaseModel):
    statusId: str | None = None
    type: IterationType | None = None
    title: str | None = None
    description: str | None = None
    goal: str | None = None
    startDate: datetime | None = None
    endDate: datetime | None = None


class IterationRead(IterationBase):
    id: str
    spaceId: str
    statusId: str
    createdAt: datetime
    updatedAt: datetime

    model_config = {"from_attributes": True}


IterationPage = CursorPage[IterationRead]