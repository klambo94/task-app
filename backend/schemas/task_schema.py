from datetime import datetime
from typing import Optional
from enums import Status
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
    created_at: datetime
    updated_at: datetime
    model_config = {"from_attributes": True}