from sqlalchemy import Column, String, ForeignKey, Enum
from sqlalchemy.orm import relationship

from app.core.database import Base
from app.models.enums import ActivityField
from app.models.mixins.timestamp_mixin import TimestampMixin

class ThreadActivity(TimestampMixin, Base):
    """
    Immutable audit log entry for a thread. One row is written every time a
    tracked field changes. Used to render the activity timeline in the thread
    detail view.
    """
    __tablename__ = "thread_activity"

    id = Column(String, primary_key=True, doc="Internal PK; set via generate_id().")
    threadId = Column(String, ForeignKey("thread.id", ondelete="CASCADE"), nullable=False,
                      doc="FK to the thread that was changed.")
    actorId = Column(String, ForeignKey("user.id", ondelete="RESTRICT"), nullable=False,
                     doc="FK to the user who made the change.")
    field = Column(
        Enum(ActivityField), nullable=False,
        doc="The field that was changed.",
    )
    oldValue = Column(String, nullable=True, doc="Serialised previous value of the field. NULL for creation events.")
    newValue = Column(String, nullable=True, doc="Serialised new value of the field. NULL for deletion events.")

    thread = relationship("Thread", back_populates="activities")
    actor = relationship("User", back_populates="activities")
