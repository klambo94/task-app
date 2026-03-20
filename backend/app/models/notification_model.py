from sqlalchemy import Column, String, ForeignKey, Enum, Boolean
from sqlalchemy.orm import relationship

from app.core.database import Base
from app.models.enums import NotificationType
from app.models.mixins.timestamp_mixin import TimestampMixin

class Notification(TimestampMixin, Base):
    """
    Per-user notification record. Written at event time by the event handlers
    and consumed by the in-app notification centre.
    """
    __tablename__ = "notification"

    id = Column(String, primary_key=True, doc="Internal PK; set via generate_id().")
    userId = Column(String, ForeignKey("user.id", ondelete="CASCADE"), nullable=False,
                    doc="FK to the user this notification belongs to.")
    type = Column(
        Enum(NotificationType), nullable=False,
        doc="The notification event type, used to render the correct message template.",
    )
    resourceId = Column(String, nullable=False,
                        doc="ID of the resource this notification refers to (e.g. a thread id).")
    resourceType = Column(String, nullable=False, doc="Type name of the resource (e.g. 'thread', 'sprint').")
    isRead = Column(
        Boolean, nullable=False, default=False,
        doc="Whether the user has seen/dismissed this notification.",
    )

    user = relationship("User", back_populates="notifications")
