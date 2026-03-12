from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
from models.thread_model import ThreadPriority
from schemas.label_schema import LabelResponse
from schemas.user_schema import UserResponse
from schemas.status_schema import StatusResponse


class ThreadCreate(BaseModel):
    title: str
    spaceId: str
    statusId: str
    description: Optional[str] = None
    priority: ThreadPriority = ThreadPriority.NO_PRIORITY
    sprintId: Optional[str] = None
    parentId: Optional[str] = None
    reporterId: Optional[str] = None
    reviewerId: Optional[str] = None
    dueDate: Optional[datetime] = None


class ThreadUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    statusId: Optional[str] = None
    priority: Optional[ThreadPriority] = None
    sprintId: Optional[str] = None
    parentId: Optional[str] = None
    reporterId: Optional[str] = None
    reviewerId: Optional[str] = None
    dueDate: Optional[datetime] = None


class ThreadFilter(BaseModel):
    spaceId: Optional[str] = None
    sprintId: Optional[str] = None
    statusId: Optional[str] = None
    assigneeId: Optional[str] = None
    labelId: Optional[str] = None
    priority: Optional[ThreadPriority] = None
    parentId: Optional[str] = None  # None = top-level only, set to filter subtasks


class ThreadResponse(BaseModel):
    id: str
    title: str
    description: Optional[str] = None
    priority: ThreadPriority
    spaceId: str
    statusId: str
    sprintId: Optional[str] = None
    parentId: Optional[str] = None
    reporterId: Optional[str] = None
    reviewerId: Optional[str] = None
    dueDate: Optional[datetime] = None
    createdAt: datetime
    updatedAt: datetime

    model_config = {"from_attributes": True}


class ThreadDetailResponse(ThreadResponse):
    """Full response with nested relationships."""
    status: Optional[StatusResponse] = None
    assignees: List[UserResponse] = []
    labels: List[LabelResponse] = []
    subtasks: List["ThreadResponse"] = []

    model_config = {"from_attributes": True}
# If I run into isssues with this schema use this
# ThreadDetailResponse.model_rebuild()