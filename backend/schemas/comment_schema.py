from pydantic import BaseModel
from datetime import datetime


class CommentCreate(BaseModel):
    content: str
    threadId: str
    authorId: str


class CommentUpdate(BaseModel):
    content: str


class CommentResponse(BaseModel):
    id: str
    content: str
    threadId: str
    authorId: str
    createdAt: datetime
    updatedAt: datetime

    model_config = {"from_attributes": True}