
from database import Base
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class Comment(Base):
    __tablename__ = "comments"
    id = Column(String, primary_key=True)
    content = Column(String, nullable=False)
    threadId = Column(String, ForeignKey("threads.id", ondelete="CASCADE"), nullable=False)
    authorId = Column(String, ForeignKey("users.id"), nullable=False)
    createdAt = Column(DateTime(), server_default=func.now())
    updatedAt = Column(DateTime(), server_default=func.now(), onupdate=func.now())

    thread = relationship("Thread", back_populates="comments")
    author = relationship("User", back_populates="comments")