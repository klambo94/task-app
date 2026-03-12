from database import Base
from sqlalchemy import Column, String, DateTime, ForeignKey, Enum as SAEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from enums import ThreadPriority


class Thread(Base):
    __tablename__ = "threads"
    id = Column(String, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    priority = Column(SAEnum(ThreadPriority), default=ThreadPriority.NO_PRIORITY)
    spaceId = Column(String, ForeignKey("spaces.id", ondelete="CASCADE"), nullable=False)
    statusId = Column(String, ForeignKey("statuses.id", ondelete="SET NULL"), nullable=True)
    sprintId = Column(String, ForeignKey("sprints.id", ondelete="SET NULL"), nullable=True)
    parentId = Column(String, ForeignKey("threads.id", ondelete="CASCADE"), nullable=True)
    reporterId = Column(String, ForeignKey("users.id"), nullable=True)
    reviewerId = Column(String, ForeignKey("users.id"), nullable=True)
    dueDate = Column(DateTime(), nullable=True)
    createdAt = Column(DateTime(), server_default=func.now())
    updatedAt = Column(DateTime(), server_default=func.now(), onupdate=func.now())

    space = relationship("Space", back_populates="threads")
    status = relationship("Status", back_populates="threads")
    sprint = relationship("Sprint", back_populates="threads")
    parent = relationship("Thread", remote_side="Thread.id", back_populates="subtasks")
    subtasks = relationship("Thread", back_populates="parent")
    assignees = relationship("ThreadAssignee", back_populates="thread")
    labels = relationship("ThreadLabel", back_populates="thread")
    comments = relationship("Comment", back_populates="thread")
    reporter = relationship("User", foreign_keys="Thread.reporterId", back_populates="reported_threads")
    reviewer = relationship("User", foreign_keys="Thread.reviewerId", back_populates="reviewing_threads")


class ThreadAssignee(Base):
    __tablename__ = "thread_assignees"
    threadId = Column(String, ForeignKey("threads.id", ondelete="CASCADE"), primary_key=True)
    userId = Column(String, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    assignedAt = Column(DateTime(), server_default=func.now())

    thread = relationship("Thread", back_populates="assignees")
    user = relationship("User", back_populates="assigned_threads")


class ThreadLabel(Base):
    __tablename__ = "thread_labels"
    threadId = Column(String, ForeignKey("threads.id", ondelete="CASCADE"), primary_key=True)
    labelId = Column(String, ForeignKey("labels.id", ondelete="CASCADE"), primary_key=True)

    thread = relationship("Thread", back_populates="labels")
    label = relationship("Label", back_populates="threads")