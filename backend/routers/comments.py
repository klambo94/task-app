import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from dependencies.auth import get_current_user
from repositories import comment_repository, access_repository
from schemas import CommentCreate, CommentUpdate, CommentResponse
from schemas.shared import DataResponse

log = logging.getLogger(__name__)
router = APIRouter(prefix="/api", tags=["comments"])


@router.get("/threads/{thread_id}/comments", response_model=DataResponse[list[CommentResponse]])
def get_comments(
    thread_id: str,
    current_user=Depends(get_current_user),
    session: Session = Depends(get_db)
):
    if not access_repository.can_access_thread(current_user.id, thread_id, session):
        raise HTTPException(status_code=403, detail="Access denied")

    comments = comment_repository.get_by_thread(thread_id, session)
    return DataResponse(data=comments)


@router.post("/comments", response_model=DataResponse[CommentResponse])
def create_comment(
    comment_in: CommentCreate,
    current_user=Depends(get_current_user),
    session: Session = Depends(get_db)
):
    if not access_repository.can_access_thread(current_user.id, comment_in.threadId, session):
        raise HTTPException(status_code=403, detail="Access denied")

    comment_in = CommentCreate(
        content=comment_in.content,
        threadId=comment_in.threadId,
        authorId=current_user.id,
    )
    comment = comment_repository.create(comment_in, session)
    return DataResponse(data=comment)


@router.patch("/comments/{comment_id}", response_model=DataResponse[CommentResponse])
def update_comment(
    comment_id: str,
    comment_in: CommentUpdate,
    current_user=Depends(get_current_user),
    session: Session = Depends(get_db)
):
    comment = comment_repository.get_by_id(comment_id, session)
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    if comment.authorId != current_user.id:
        raise HTTPException(status_code=403, detail="Can only edit your own comments")

    result = comment_repository.update(comment_id, comment_in, session)
    return DataResponse(data=result)


@router.delete("/comments/{comment_id}")
def delete_comment(
    comment_id: str,
    current_user=Depends(get_current_user),
    session: Session = Depends(get_db)
):
    comment = comment_repository.get_by_id(comment_id, session)
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    if comment.authorId != current_user.id:
        raise HTTPException(status_code=403, detail="Can only delete your own comments")

    comment_repository.delete(comment_id, session)
    return {"message": "Comment deleted"}