from pydantic import BaseModel
from datetime import datetime
from app.models.enums import ThreadPriority
from app.lib.pagination import CursorPage


class ThreadBase(BaseModel):
    title: str
    body: str | None = None
    priority: ThreadPriority = ThreadPriority.NONE
    dueDate: datetime | None = None
    sortOrder: int = 0


class ThreadCreate(ThreadBase):
    spaceId: str
    statusId: str
    reporterId: str
    assigneeId: str | None = None
    iterationId: str | None = None


class ThreadUpdate(BaseModel):
    statusId: str | None = None
    assigneeId: str | None = None
    iterationId: str | None = None
    title: str | None = None
    body: str | None = None
    priority: ThreadPriority | None = None
    dueDate: datetime | None = None
    sortOrder: int | None = None


class ThreadRead(ThreadBase):
    id: str
    spaceId: str
    statusId: str
    reporterId: str
    assigneeId: str | None
    iterationId: str | None
    createdAt: datetime
    updatedAt: datetime

    model_config = {"from_attributes": True}


ThreadPage = CursorPage[ThreadRead]