from database import Base
from sqlalchemy import Column, String, DateTime, ForeignKey, Integer, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class SprintStatus(Base):
    __tablename__ = "sprint_statuses"
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    color = Column(String, nullable=False)
    order = Column(Integer, nullable=False)
    isDefault = Column(Boolean, default=False)
    isClosed = Column(Boolean, default=False)
    spaceId = Column(String, ForeignKey("spaces.id", ondelete="CASCADE"), nullable=False)

    space = relationship("Space", back_populates="sprintStatuses")
    sprints = relationship("Sprint", back_populates="status")


class Sprint(Base):
    __tablename__ = "sprints"
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    goal = Column(String, nullable=True)
    statusId = Column(String, ForeignKey("sprint_statuses.id", ondelete="SET NULL"), nullable=True)
    spaceId = Column(String, ForeignKey("spaces.id", ondelete="CASCADE"), nullable=False)
    startDate = Column(DateTime(), nullable=True)
    endDate = Column(DateTime(), nullable=True)
    createdAt = Column(DateTime(), server_default=func.now())
    updatedAt = Column(DateTime, server_default=func.now(), onupdate=func.now())  # ← missing

    space = relationship("Space", back_populates="sprints")
    status = relationship("SprintStatus", back_populates="sprints")
    threads = relationship("Thread", back_populates="sprint")