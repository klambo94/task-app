from sqlalchemy import Column, DateTime, Enum, ForeignKey, String, Text
from sqlalchemy.orm import relationship

from app.core.database import Base
from app.models.mixins.timestamp_mixin import TimestampMixin
from app.models.enums import IterationType


class Iteration(TimestampMixin, Base):
    """
    A time-boxed unit of work within a space. The `type` field makes this
    model methodology-agnostic — a sprint, release, phase, or milestone are
    all iterations with different types.
    """
    __tablename__ = "iteration"

    id = Column(String, primary_key=True, doc="Internal PK; set via generate_id().")
    spaceId = Column(String, ForeignKey("space.id", ondelete="CASCADE"), nullable=False, doc="FK to the owning space.")
    statusId = Column(String, ForeignKey("status.id", ondelete="RESTRICT"), nullable=False,
                      doc="FK to the iteration's current status.")
    type = Column(Enum(IterationType), nullable=False, default=IterationType.SPRINT,
                  doc="Methodology type: sprint, release, phase, or milestone.")
    title = Column(String, nullable=False, doc="Short name for the iteration (e.g. 'Sprint 4', 'v2.0 Release').")
    description = Column(Text, nullable=True, doc="Longer description of the iteration's scope.")
    goal = Column(Text, nullable=True, doc="The iteration goal statement, shown at the top of the board.")
    startDate = Column(DateTime(timezone=True), nullable=True, doc="Planned start date.")
    endDate = Column(DateTime(timezone=True), nullable=True, doc="Planned end date.")

    # Relationships
    space = relationship("Space", back_populates="iterations")
    status = relationship("Status", back_populates="iterations")
    threads = relationship("Thread", back_populates="iteration")