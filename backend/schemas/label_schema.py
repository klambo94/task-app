from pydantic import BaseModel
from typing import Optional


class LabelCreate(BaseModel):
    name: str
    spaceId: str
    color: Optional[str] = None


class LabelUpdate(BaseModel):
    name: Optional[str] = None
    color: Optional[str] = None
    spaceId: Optional[str] = None

class LabelResponse(BaseModel):
    id: str
    name: str
    spaceId: str
    color: Optional[str] = None

    model_config = {"from_attributes": True}