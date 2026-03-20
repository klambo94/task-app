
from app.models.enums import StatusCategory

from sqlalchemy import Column, String, ForeignKey, Enum, Integer
from sqlalchemy.orm import relationship

from app.core.database import Base
from app.models.mixins.timestamp_mixin import TimestampMixin


class Status(TimestampMixin, Base):
    """
    A workflow status scoped to a space (e.g. "In Review", "Blocked").
    Both threads and sprints reference a status.
    """
    __tablename__ = "status"

    id = Column(String, primary_key=True, doc="Internal PK; set via generate_id().")
    spaceId = Column(String, ForeignKey("space.id", ondelete="CASCADE"), nullable=False, doc="FK to the owning space.")
    name = Column(String, nullable=False, doc="Display name of the status (e.g. 'In Review').")
    colour = Column(
        String, nullable=False, default="#6B7280",
        doc="Hex colour string used to render the status badge in the UI.",
    )
    category = Column(
        Enum(StatusCategory), nullable=False, default=StatusCategory.TODO,
        doc="Semantic category used for rollups and board column grouping.",
    )
    sortOrder = Column(
        Integer, nullable=False, default=0,
        doc="Display order of this status within the space's workflow.",
    )

    space = relationship("Space", back_populates="statuses")
    threads = relationship("Thread", back_populates="status")
    iterations = relationship("Iteration", back_populates="status")