from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from models.space_model import SpaceVisibility


class SpaceCreate(BaseModel):
    name: str
    ownerId: str
    organizationId: Optional[str] = None
    description: Optional[str] = None
    visibility: SpaceVisibility = SpaceVisibility.PERSONAL


class SpaceUpdate(BaseModel):
    name: Optional[str] = None
    visibility: Optional[SpaceVisibility] = None


class SpaceResponse(BaseModel):
    id: str
    name: str
    ownerId: str
    organizationId: Optional[str] = None
    visibility: SpaceVisibility
    createdAt: datetime
    updatedAt: datetime

    model_config = {"from_attributes": True}