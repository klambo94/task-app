from typing import Optional


from models import Status
from datetime import datetime, timezone
from pydantic import BaseModel, Field

class TaskCreate(BaseModel):
    name: str
    description: Optional[str] = None
    status: Status
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class TaskUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[Status] = None
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class TaskResponse(BaseModel):
    name: str
    description: Optional[str] = None
    status: Status
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}