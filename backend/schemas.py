from typing import Optional

from models import Status
from pydantic import BaseModel

class TaskCreate(BaseModel):
    name: str
    description: Optional[str] = None
    status: Status

class TaskUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[Status] = None

class TaskResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    status: Status

    model_config = {"from_attributes": True}