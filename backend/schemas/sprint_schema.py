from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class SprintCreate(BaseModel):
    name: str
    spaceId: str
    statusId: str
    startDate: Optional[datetime] = None
    endDate: Optional[datetime] = None


class SprintUpdate(BaseModel):
    name: Optional[str] = None
    statusId: Optional[str] = None
    startDate: Optional[datetime] = None
    endDate: Optional[datetime] = None


class SprintResponse(BaseModel):
    id: str
    name: str
    spaceId: str
    statusId: str
    startDate: Optional[datetime] = None
    endDate: Optional[datetime] = None
    createdAt: datetime
    updatedAt: datetime

    model_config = {"from_attributes": True}


class SprintStatusCreate(BaseModel):
    name: str
    spaceId: Optional[str] = None  # ← optional, injected by router from path param
    color: Optional[str] = None
    order: int = 0
    isDefault: bool = False
    isClosed: bool = False
    goal: Optional[str] = None

class SprintStatusUpdate(BaseModel):
    name: Optional[str] = None
    color: Optional[str] = None
    order: Optional[int] = None
    isDefault: Optional[bool] = None
    isClosed: Optional[bool] = None


class SprintStatusResponse(BaseModel):
    id: str
    name: str
    spaceId: str
    color: Optional[str] = None
    order: int
    isDefault: bool
    isClosed: bool

    model_config = {"from_attributes": True}