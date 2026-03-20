from sqlalchemy import Column, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

from app.core.database import Base
from app.models import thread_label
from app.models.mixins import TimestampMixin

class Label(TimestampMixin, Base):
    """
    A coloured tag scoped to a space. Threads can carry multiple labels.
    """
    __tablename__ = "label"

    id = Column(String, primary_key=True, doc="Internal PK; set via generate_id().")
    spaceId = Column(String, ForeignKey("space.id", ondelete="CASCADE"), nullable=False, doc="FK to the owning space.")
    name = Column(String, nullable=False, doc="Display name of the label (e.g. 'bug', 'feature').")
    colour = Column(
        String, nullable=False, default="#6B7280",
        doc="Hex colour string used to render the label chip.",
    )

    __table_args__ = (UniqueConstraint("spaceId", "name", name="uq_label_name"),)

    space = relationship("Space", back_populates="labels")
    threads = relationship("Thread", secondary=thread_label, back_populates="labels")
