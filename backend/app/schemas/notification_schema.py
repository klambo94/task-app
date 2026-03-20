from pydantic import BaseModel
from datetime import datetime
from app.models.enums import NotificationType
from app.lib.pagination import CursorPage


class NotificationBase(BaseModel):
    type: NotificationType
    resourceId: str
    resourceType: str
    isRead: bool = False


class NotificationCreate(NotificationBase):
    userId: str


class NotificationUpdate(BaseModel):
    isRead: bool


class NotificationRead(NotificationBase):
    id: str
    userId: str
    createdAt: datetime
    updatedAt: datetime

    model_config = {"from_attributes": True}


NotificationPage = CursorPage[NotificationRead]