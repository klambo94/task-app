from pydantic import BaseModel
from datetime import datetime
from app.models.enums import ActivityField


class ThreadActivityBase(BaseModel):
    field: ActivityField
    oldValue: str | None = None
    newValue: str | None = None


class ThreadActivityCreate(ThreadActivityBase):
    threadId: str
    actorId: str


class ThreadActivityRead(ThreadActivityBase):
    id: str
    threadId: str
    actorId: str
    createdAt: datetime

    model_config = {"from_attributes": True}