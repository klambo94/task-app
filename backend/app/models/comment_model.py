from sqlalchemy import Column, String, ForeignKey, Text
from sqlalchemy.orm import relationship

from app.core.database import Base
from app.models.mixins import TimestampMixin


class Comment(TimestampMixin, Base):
    """
    A comment on a thread. Supports attachments via the Attachment model.
    """
    __tablename__ = "comment"

    id = Column(String, primary_key=True, doc="Internal PK; set via generate_id().")
    threadId = Column(String, ForeignKey("thread.id", ondelete="CASCADE"), nullable=False,
                      doc="FK to the parent thread.")
    authorId = Column(String, ForeignKey("user.id", ondelete="RESTRICT"), nullable=False,
                      doc="FK to the user who wrote the comment.")
    body = Column(Text, nullable=False, doc="Rich-text body of the comment.")

    thread = relationship("Thread", back_populates="comments")
    author = relationship("User", back_populates="comments")
    attachments = relationship("Attachment", back_populates="comment")
