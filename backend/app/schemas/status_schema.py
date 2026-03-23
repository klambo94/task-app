from pydantic import BaseModel
from datetime import datetime
from app.models.enums import StatusCategory
from app.lib.pagination import CursorPage


class StatusBase(BaseModel):
    name: str
    color: str = "#6B7280"
    category: StatusCategory = StatusCategory.TODO
    sortOrder: int = 0


class StatusCreate(StatusBase):
    spaceId: str


class StatusUpdate(BaseModel):
    name: str | None = None
    color: str | None = None
    category: StatusCategory | None = None
    sortOrder: int | None = None


class StatusRead(StatusBase):
    id: str
    spaceId: str
    createdAt: datetime
    updatedAt: datetime

    model_config = {"from_attributes": True}


StatusPage = CursorPage[StatusRead]