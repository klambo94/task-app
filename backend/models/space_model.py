import enum

from sqlalchemy.orm import relationship


from database import Base
from sqlalchemy import Column, String, DateTime, Enum as SAEnum, Boolean, func, ForeignKey

from enums import SpaceVisibility


class Space(Base):
    __tablename__ = "spaces"
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    visibility = Column(SAEnum(SpaceVisibility), default=SpaceVisibility.PERSONAL)
    organizationId = Column(String, ForeignKey("organizations.id", ondelete="CASCADE"), nullable=True)
    ownerId = Column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    createdAt = Column(DateTime(), server_default=func.now())
    updatedAt = Column(DateTime(), server_default=func.now(), onupdate=func.now())

    organization = relationship("Organization", back_populates="spaces")
    owner = relationship("User", back_populates="spaces")
    statuses = relationship("Status", back_populates="space", cascade="all, delete-orphan")
    sprintStatuses = relationship("SprintStatus", back_populates="space", cascade="all, delete-orphan")
    sprints = relationship("Sprint", back_populates="space", cascade="all, delete-orphan")
    threads = relationship("Thread", back_populates="space", cascade="all, delete-orphan")
    labels = relationship("Label", back_populates="space", cascade="all, delete-orphan")
