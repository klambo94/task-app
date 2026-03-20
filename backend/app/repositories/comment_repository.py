from datetime import datetime, timezone
from sqlalchemy.orm import Session

from app.lib import CursorPage, generate_id, paginate
from app.models.comment_model import Comment


class CommentRepository:

    def __init__(self, db: Session):
        self.db = db

    # ------------------------------------------------------------------
    # Reads
    # ------------------------------------------------------------------

    def get_by_id(self, comment_id: str) -> Comment | None:
        return (
            self.db.query(Comment)
            .filter(Comment.id == comment_id, Comment.deletedAt.is_(None))
            .first()
        )

    def list_by_thread(
            self,
            thread_id: str,
            cursor: str | None = None,
            limit: int = 20,
    ) -> CursorPage:
        query = (
            self.db.query(Comment)
            .filter(Comment.threadId == thread_id, Comment.deletedAt.is_(None))
            .order_by(Comment.createdAt.asc(), Comment.id.asc())
        )
        return paginate(query, cursor, limit)

    # ------------------------------------------------------------------
    # Writes
    # ------------------------------------------------------------------

    def create(self, thread_id: str, author_id: str, body: str) -> Comment:
        comment = Comment(
            id=generate_id(),
            threadId=thread_id,
            authorId=author_id,
            body=body,
        )
        self.db.add(comment)
        self.db.flush()
        return comment

    def update(self, comment: Comment, body: str) -> Comment:
        comment.body = body
        self.db.flush()
        return comment

    def soft_delete(self, comment: Comment) -> Comment:
        comment.deletedAt = datetime.now(timezone.utc)
        self.db.flush()
        return comment