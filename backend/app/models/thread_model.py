from sqlalchemy import Column, String, ForeignKey, DateTime, Integer, Text, Enum, Table
from sqlalchemy.orm import relationship

from app.core.database import Base
from app.models import ThreadPriority
from app.models.mixins.timestamp_mixin import TimestampMixin


# Many-to-many between Thread and Label.
thread_label = Table(
    "thread_label",
    Base.metadata,
    Column(
        "threadId",
        String,
        ForeignKey("thread.id", ondelete="CASCADE"),
        primary_key=True,
        doc="FK to the thread.",
    ),
    Column(
        "labelId",
        String,
        ForeignKey("label.id", ondelete="CASCADE"),
        primary_key=True,
        doc="FK to the label.",
    ),
)

class Thread(TimestampMixin, Base):
    """
    The core work item in Psinaptic (analogous to a Jira issue or Trello card).
    """
    __tablename__ = "thread"

    id = Column(String, primary_key=True, doc="Internal PK; set via generate_id().")
    spaceId = Column(String, ForeignKey("space.id", ondelete="CASCADE"), nullable=False, doc="FK to the owning space.")
    statusId = Column(String, ForeignKey("status.id", ondelete="RESTRICT"), nullable=False,
                      doc="FK to the thread's current status.")
    reporterId = Column(String, ForeignKey("user.id", ondelete="RESTRICT"), nullable=False,
                        doc="FK to the user who created the thread.")
    assigneeId = Column(String, ForeignKey("user.id", ondelete="SET NULL"), nullable=True,
                        doc="FK to the user currently assigned to the thread. NULL = unassigned.")
    iterationId = Column(String, ForeignKey("iteration.id", ondelete="SET NULL"), nullable=True,
                         doc="FK to the active iteration. NULL = backlog.")
    title = Column(String, nullable=False, doc="One-line summary of the thread.")
    body = Column(Text, nullable=True, doc="Rich-text description of the thread.")
    priority = Column(

        Enum(ThreadPriority), nullable=False, default=ThreadPriority.NONE,
        doc="Priority level used for sorting and filtering.",
    )
    dueDate = Column(DateTime(timezone=True), nullable=True, doc="Optional due date for the thread.")
    sortOrder = Column(
        Integer, nullable=False, default=0,
        doc="Manual sort position within a status column on the board view.",
    )

    # Relationships
    space = relationship("Space", back_populates="threads")
    status = relationship("Status", back_populates="threads")
    reporter = relationship("User", back_populates="reportedThreads", foreign_keys=[reporterId])
    assignee = relationship("User", back_populates="assignedThreads", foreign_keys=[assigneeId])
    iteration = relationship("Iteration", back_populates="threads", cascade="all, delete-orphan")
    comments = relationship("Comment", back_populates="thread", cascade="all, delete-orphan")
    labels = relationship("Label", secondary=thread_label, back_populates="threads")
    attachments = relationship("Attachment", back_populates="thread")
    activities = relationship("ThreadActivity", back_populates="thread", cascade="all, delete-orphan")
