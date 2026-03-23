
from pydantic import BaseModel
from datetime import datetime
from app.lib.pagination import CursorPage


class LabelBase(BaseModel):
    name: str
    color: str = "#6B7280"


class LabelCreate(LabelBase):
    spaceId: str


class LabelUpdate(BaseModel):
    name: str | None = None
    color: str | None = None


class LabelRead(LabelBase):
    id: str
    spaceId: str
    createdAt: datetime
    updatedAt: datetime

    model_config = {"from_attributes": True}


LabelPage = CursorPage[LabelRead]