# app/schemas/comment_schema.py

from pydantic import BaseModel
from datetime import datetime
from app.lib.pagination import CursorPage


# ------------------------------------------------------------------
# Comment
# ------------------------------------------------------------------

class CommentBase(BaseModel):
    body: str


class CommentCreate(CommentBase):
    threadId: str
    authorId: str


class CommentUpdate(BaseModel):
    body: str


class CommentRead(CommentBase):
    id: str
    threadId: str
    authorId: str
    createdAt: datetime
    updatedAt: datetime

    model_config = {"from_attributes": True}


CommentPage = CursorPage[CommentRead]


# ------------------------------------------------------------------
# Attachment
# ------------------------------------------------------------------

class AttachmentBase(BaseModel):
    filename: str
    fileUrl: str
    fileSize: int
    mimeType: str


class AttachmentCreate(AttachmentBase):
    uploadedById: str
    threadId: str | None = None
    commentId: str | None = None


class AttachmentUpdate(BaseModel):
    pass


class AttachmentRead(AttachmentBase):
    id: str
    uploadedById: str
    threadId: str | None
    commentId: str | None
    createdAt: datetime
    updatedAt: datetime

    model_config = {"from_attributes": True}


AttachmentPage = CursorPage[AttachmentRead]