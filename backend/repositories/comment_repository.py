import logging

from sqlalchemy import Sequence
from sqlalchemy.orm import Session

from models import Comment
from schemas.comment_schema import CommentCreate, CommentUpdate
from utils import generate_id

log = logging.getLogger(__name__)


def create(comment_in: CommentCreate, session: Session) -> Comment:
    log.debug(f"create_comment for thread: {comment_in.threadId}")
    comment = Comment(
        id=generate_id(),
        content=comment_in.content,
        threadId=comment_in.threadId,
        authorId=comment_in.authorId,
    )
    session.add(comment)
    session.commit()
    session.refresh(comment)
    return comment


def get_by_id(comment_id: str, session: Session) -> Comment | None:
    return session.query(Comment).filter(Comment.id == comment_id).first()


def get_by_thread(thread_id: str, session: Session) -> Sequence[Comment]:
    return session.query(Comment).filter(
        Comment.threadId == thread_id
    ).order_by(Comment.createdAt).all()


def update(comment_id: str, comment_in: CommentUpdate, session: Session) -> Comment | None:
    log.debug(f"update_comment: {comment_id}")
    comment = get_by_id(comment_id, session)

    if not comment:
        log.info(f"Comment not found: {comment_id}")
        return None

    comment.content = comment_in.content
    session.commit()
    session.refresh(comment)
    return comment


def delete(comment_id: str, session: Session) -> bool:
    log.debug(f"delete_comment: {comment_id}")
    comment = get_by_id(comment_id, session)

    if not comment:
        log.info(f"Comment not found: {comment_id}")
        return False

    session.delete(comment)
    session.commit()
    return True