from database import Base
from sqlalchemy import Column, String, DateTime, ForeignKey, Integer, Boolean, Enum as SAEnum
from sqlalchemy.orm import relationship


from enums import StatusCategory


class Status(Base):
    __tablename__ = "statuses"
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    color = Column(String, nullable=False)
    icon = Column(String, nullable=True)
    order = Column(Integer, nullable=False)
    isDefault = Column(Boolean, default=False)
    isClosed = Column(Boolean, default=False)
    category = Column(SAEnum(StatusCategory), nullable=False)
    spaceId = Column(String, ForeignKey("spaces.id", ondelete="CASCADE"), nullable=False)

    space = relationship("Space", back_populates="statuses")
    threads = relationship("Thread", back_populates="status")

