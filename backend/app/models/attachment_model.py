from sqlalchemy import Column, String, ForeignKey, Integer
from sqlalchemy.orm import relationship

from app.core.database import Base
from app.models.mixins.timestamp_mixin import TimestampMixin

class Attachment(TimestampMixin, Base):
    """
    A file attached to either a thread or a comment.

    Exactly one of threadId / commentId must be set. This is enforced at the
    application layer in the repository before insert.
    """
    __tablename__ = "attachment"

    id = Column(String, primary_key=True, doc="Internal PK; set via generate_id().")
    threadId = Column(String, ForeignKey("thread.id", ondelete="CASCADE"), nullable=True,
                      doc="FK to the parent thread. Mutually exclusive with commentId.")
    commentId = Column(String, ForeignKey("comment.id", ondelete="CASCADE"), nullable=True,
                       doc="FK to the parent comment. Mutually exclusive with threadId.")
    uploadedById = Column(String, ForeignKey("user.id", ondelete="RESTRICT"), nullable=False,
                          doc="FK to the user who uploaded the file.")
    filename = Column(String, nullable=False, doc="Original filename as uploaded by the user.")
    fileUrl = Column(String, nullable=False, doc="Storage URL (e.g. S3 presigned or CDN URL) of the uploaded file.")
    fileSize = Column(Integer, nullable=False, doc="File size in bytes.")
    mimeType = Column(String, nullable=False, doc="MIME type of the file (e.g. 'image/png', 'application/pdf').")

    thread = relationship("Thread", back_populates="attachments")
    comment = relationship("Comment", back_populates="attachments")
    uploadedBy = relationship("User", back_populates="attachments")
