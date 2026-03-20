from datetime import datetime, timezone
from sqlalchemy.orm import Session
from app.models.attachment_model import Attachment
from app.lib import CursorPage, generate_id, paginate


def _validate_parent(thread_id: str | None, comment_id: str | None) -> None:
    """Enforce the one-parent rule at the application layer."""
    if thread_id is None and comment_id is None:
        raise ValueError("Attachment must belong to either a thread or a comment.")
    if thread_id is not None and comment_id is not None:
        raise ValueError("Attachment cannot belong to both a thread and a comment.")


class AttachmentRepository:

    def __init__(self, db: Session):
        self.db = db

    # ------------------------------------------------------------------
    # Reads
    # ------------------------------------------------------------------

    def get_by_id(self, attachment_id: str) -> Attachment | None:
        return (
            self.db.query(Attachment)
            .filter(Attachment.id == attachment_id, Attachment.deletedAt.is_(None))
            .first()
        )

    def list_by_thread(
            self,
            thread_id: str,
            cursor: str | None = None,
            limit: int = 20,
    ) -> CursorPage:
        query = (
            self.db.query(Attachment)
            .filter(Attachment.threadId == thread_id, Attachment.deletedAt.is_(None))
            .order_by(Attachment.createdAt.desc(), Attachment.id.desc())
        )
        return paginate(query, cursor, limit)

    def list_by_comment(
            self,
            comment_id: str,
            cursor: str | None = None,
            limit: int = 20,
    ) -> CursorPage:
        query = (
            self.db.query(Attachment)
            .filter(Attachment.commentId == comment_id, Attachment.deletedAt.is_(None))
            .order_by(Attachment.createdAt.desc(), Attachment.id.desc())
        )
        return paginate(query, cursor, limit)

    # ------------------------------------------------------------------
    # Writes
    # ------------------------------------------------------------------

    def create_for_thread(
            self,
            thread_id: str,
            uploaded_by_id: str,
            filename: str,
            file_url: str,
            file_size: int,
            mime_type: str,
    ) -> Attachment:
        _validate_parent(thread_id=thread_id, comment_id=None)
        attachment = Attachment(
            id=generate_id(),
            threadId=thread_id,
            commentId=None,
            uploadedById=uploaded_by_id,
            filename=filename,
            fileUrl=file_url,
            fileSize=file_size,
            mimeType=mime_type,
        )
        self.db.add(attachment)
        self.db.flush()
        return attachment

    def create_for_comment(
            self,
            comment_id: str,
            uploaded_by_id: str,
            filename: str,
            file_url: str,
            file_size: int,
            mime_type: str,
    ) -> Attachment:
        _validate_parent(thread_id=None, comment_id=comment_id)
        attachment = Attachment(
            id=generate_id(),
            threadId=None,
            commentId=comment_id,
            uploadedById=uploaded_by_id,
            filename=filename,
            fileUrl=file_url,
            fileSize=file_size,
            mimeType=mime_type,
        )
        self.db.add(attachment)
        self.db.flush()
        return attachment

    def soft_delete(self, attachment: Attachment) -> Attachment:
        attachment.deletedAt = datetime.now(timezone.utc)
        self.db.flush()
        return attachment
