from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_current_user
from app.models import User
from app.repositories import CommentRepository, ThreadRepository
from app.schemas import CommentRead, CommentCreate, CommentUpdate, CommentPage
from app.schemas.response_schema import DataResponse, MessageResponse

thread_comment_router = APIRouter(prefix="/threads", tags=["Comments"])
comment_router = APIRouter(prefix="/comments", tags=["Comments"])


@thread_comment_router.get("/{thread_id}/comments", response_model=DataResponse[CommentPage])
def list_comments(
    thread_id: str,
    cursor: str | None = Query(default=None),
    limit: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    thread_repo = ThreadRepository(db)
    comment_repo = CommentRepository(db)

    thread = thread_repo.get_by_id(thread_id)
    if not thread:
        raise HTTPException(status_code=404, detail="Thread not found")

    return DataResponse(data=comment_repo.list_by_thread(thread_id=thread_id, cursor=cursor, limit=limit))


@thread_comment_router.post("/{thread_id}/comments", response_model=DataResponse[CommentRead])
def create_comment(
    thread_id: str,
    body: CommentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    thread_repo = ThreadRepository(db)
    comment_repo = CommentRepository(db)

    thread = thread_repo.get_by_id(thread_id)
    if not thread:
        raise HTTPException(status_code=404, detail="Thread not found")

    comment = comment_repo.create(thread_id=thread_id, author_id=current_user.id, body=body.body)
    db.commit()
    return DataResponse(data=comment)


@comment_router.get("/{comment_id}", response_model=DataResponse[CommentRead])
def get_comment(
    comment_id: str,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    comment_repo = CommentRepository(db)
    comment = comment_repo.get_by_id(comment_id)
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    return DataResponse(data=comment)


@comment_router.patch("/{comment_id}", response_model=DataResponse[CommentRead])
def update_comment(
    comment_id: str,
    body: CommentUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    comment_repo = CommentRepository(db)
    comment = comment_repo.get_by_id(comment_id)
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")

    comment = comment_repo.update(comment, body=body.body)
    db.commit()
    return DataResponse(data=comment)


@comment_router.delete("/{comment_id}", response_model=MessageResponse)
def delete_comment(
    comment_id: str,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    comment_repo = CommentRepository(db)
    comment = comment_repo.get_by_id(comment_id)
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")

    comment_repo.soft_delete(comment)
    db.commit()
    return MessageResponse(message="Comment deleted successfully")