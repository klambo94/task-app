from sqlalchemy import UniqueConstraint, Column, String, ForeignKey
from sqlalchemy.orm import relationship

from app.core.database import Base
from app.models.mixins.timestamp_mixin import TimestampMixin

class Space(TimestampMixin, Base):
    """
    A workspace within an org. Threads, sprints, statuses, and labels are all
    scoped to a space so that different teams can operate independently.
    """
    __tablename__ = "space"

    id = Column(String, primary_key=True, doc="Internal PK; set via generate_id().")
    orgId = Column(String, ForeignKey("org.id", ondelete="CASCADE"), nullable=False, doc="FK to the parent org.")
    name = Column(String, nullable=False, doc="Human-readable space name.")
    slug = Column(
        String, nullable=False, index=True,
        doc="URL-safe identifier, unique within the org.",
    )

    __table_args__ = (UniqueConstraint("orgId", "slug", name="uq_space_slug"),)

    # Relationships
    org = relationship("Org", back_populates="spaces")
    threads = relationship("Thread", back_populates="space", cascade="all, delete-orphan")
    iterations = relationship("Iteration", back_populates="space", cascade="all, delete-orphan")
    statuses = relationship("Status", back_populates="space", cascade="all, delete-orphan")
    labels = relationship("Label", back_populates="space", cascade="all, delete-orphan")