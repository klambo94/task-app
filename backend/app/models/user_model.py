from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from app.core.database import Base
from app.models.mixins.timestamp_mixin import TimestampMixin


class User(TimestampMixin, Base):
    """
    Local mirror of a Kinde identity record.

    Psinaptic does not own auth — Kinde does. This table exists so that domain
    models (Thread, Comment, etc.) can hold stable foreign keys without hitting
    the Kinde API on every query.
    """
    __tablename__ = "user"

    id = Column(String, primary_key=True, doc="Internal PK; set via generate_id().")
    kindeId = Column(
        String, unique=True, nullable=False, index=True,
        doc="The Kinde `sub` claim — the stable external identity identifier.",
    )
    email = Column(
        String, unique=True, nullable=False,
        doc="User's email address, synced from Kinde on login.",
    )
    name = Column(
        String, nullable=True,
        doc="Display name synced from Kinde. Nullable until the user completes their profile.",
    )
    avatarUrl = Column(
        String, nullable=True,
        doc="URL of the user's avatar image, synced from Kinde.",
    )

    # Relationships
    orgMemberships = relationship("OrgMember", back_populates="user", cascade="all, delete-orphan")
    reportedThreads = relationship("Thread", back_populates="reporter", foreign_keys="Thread.reporterId")
    assignedThreads = relationship("Thread", back_populates="assignee", foreign_keys="Thread.assigneeId")
    comments = relationship("Comment", back_populates="author", cascade="all, delete-orphan")
    notifications = relationship("Notification", back_populates="user", cascade="all, delete-orphan")
    attributes = relationship("UserAttribute", back_populates="user", cascade="all, delete-orphan")
    attachments = relationship("Attachment", back_populates="uploadedBy")
    activities = relationship("ThreadActivity", back_populates="actor")