from pydantic import BaseModel
from datetime import datetime
from app.lib.pagination import CursorPage


class SpaceBase(BaseModel):
    name: str
    slug: str


class SpaceCreate(SpaceBase):
    orgId: str


class SpaceUpdate(BaseModel):
    name: str | None = None
    slug: str | None = None


class SpaceRead(SpaceBase):
    id: str
    orgId: str
    createdAt: datetime
    updatedAt: datetime

    model_config = {"from_attributes": True}


SpacePage = CursorPage[SpaceRead]