from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from app.core.database import Base
from app.models.mixins.timestamp_mixin import TimestampMixin


class Org(TimestampMixin, Base):
    """
    Top-level tenant. Every space, thread, and invitation belongs to an org.
    """
    __tablename__ = "org"

    id = Column(String, primary_key=True, doc="Internal PK; set via generate_id().")
    name = Column(
        String, nullable=False,
        doc="Human-readable org name shown in the UI.",
    )
    slug = Column(
        String, unique=True, nullable=False, index=True,
        doc="URL-safe identifier for the org, generated via python-slugify.",
    )

    # Relationships
    members = relationship("OrgMember", back_populates="org", cascade="all, delete-orphan")
    spaces = relationship("Space", back_populates="org", cascade="all, delete-orphan")
    invitations = relationship("Invitation", back_populates="org", cascade="all, delete-orphan")