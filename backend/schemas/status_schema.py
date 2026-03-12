from pydantic import BaseModel
from typing import Optional

from enums import StatusCategory


class StatusCreate(BaseModel):
    name: str
    spaceId: Optional[str] = None  # ← same fix
    category: StatusCategory
    color: Optional[str] = None
    icon: Optional[str] = None
    order: int = 0
    isDefault: bool = False
    isClosed: bool = False


class StatusUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[StatusCategory] = None
    color: Optional[str] = None
    icon: Optional[str] = None
    order: Optional[int] = None
    isDefault: Optional[bool] = None
    isClosed: Optional[bool] = None


class StatusReorder(BaseModel):
    # list of { id, order } to bulk update
    id: str
    order: int


class StatusResponse(BaseModel):
    id: str
    name: str
    spaceId: str
    category: StatusCategory
    color: Optional[str] = None
    icon: Optional[str] = None
    order: int
    isDefault: bool
    isClosed: bool

    model_config = {"from_attributes": True}