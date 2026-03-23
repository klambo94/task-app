
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_current_user
from app.models import User
from app.repositories import AttachmentRepository, ThreadRepository, CommentRepository
from app.schemas import AttachmentRead, AttachmentCreate, AttachmentPage
from app.schemas.response_schema import DataResponse, MessageResponse

thread_attachment_router = APIRouter(prefix="/threads", tags=["Attachments"])
comment_attachment_router = APIRouter(prefix="/comments", tags=["Attachments"])
attachment_router = APIRouter(prefix="/attachments", tags=["Attachments"])


@thread_attachment_router.get("/{thread_id}/attachments", response_model=DataResponse[AttachmentPage])
def list_thread_attachments(
    thread_id: str,
    cursor: str | None = Query(default=None),
    limit: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    thread_repo = ThreadRepository(db)
    attachment_repo = AttachmentRepository(db)

    thread = thread_repo.get_by_id(thread_id)
    if not thread:
        raise HTTPException(status_code=404, detail="Thread not found")

    return DataResponse(data=attachment_repo.list_by_thread(thread_id=thread_id, cursor=cursor, limit=limit))


@thread_attachment_router.post("/{thread_id}/attachments", response_model=DataResponse[AttachmentRead])
def create_thread_attachment(
    thread_id: str,
    body: AttachmentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    thread_repo = ThreadRepository(db)
    attachment_repo = AttachmentRepository(db)

    thread = thread_repo.get_by_id(thread_id)
    if not thread:
        raise HTTPException(status_code=404, detail="Thread not found")

    attachment = attachment_repo.create_for_thread(
        thread_id=thread_id,
        uploaded_by_id=current_user.id,
        filename=body.filename,
        file_url=body.fileUrl,
        file_size=body.fileSize,
        mime_type=body.mimeType,
    )
    db.commit()
    return DataResponse(data=attachment)


@comment_attachment_router.get("/{comment_id}/attachments", response_model=DataResponse[AttachmentPage])
def list_comment_attachments(
    comment_id: str,
    cursor: str | None = Query(default=None),
    limit: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    comment_repo = CommentRepository(db)
    attachment_repo = AttachmentRepository(db)

    comment = comment_repo.get_by_id(comment_id)
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")

    return DataResponse(data=attachment_repo.list_by_comment(comment_id=comment_id, cursor=cursor, limit=limit))


@comment_attachment_router.post("/{comment_id}/attachments", response_model=DataResponse[AttachmentRead])
def create_comment_attachment(
    comment_id: str,
    body: AttachmentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    comment_repo = CommentRepository(db)
    attachment_repo = AttachmentRepository(db)

    comment = comment_repo.get_by_id(comment_id)
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")

    attachment = attachment_repo.create_for_comment(
        comment_id=comment_id,
        uploaded_by_id=current_user.id,
        filename=body.filename,
        file_url=body.fileUrl,
        file_size=body.fileSize,
        mime_type=body.mimeType,
    )
    db.commit()
    return DataResponse(data=attachment)


@attachment_router.delete("/{attachment_id}", response_model=MessageResponse)
def delete_attachment(
    attachment_id: str,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    attachment_repo = AttachmentRepository(db)
    attachment = attachment_repo.get_by_id(attachment_id)
    if not attachment:
        raise HTTPException(status_code=404, detail="Attachment not found")

    attachment_repo.soft_delete(attachment)
    db.commit()
    return MessageResponse(message="Attachment deleted successfully")