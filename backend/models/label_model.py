from database import Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship

class Label(Base):
    __tablename__ = "labels"
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    color = Column(String, nullable=False)  # hex or oklch
    spaceId = Column(String, ForeignKey("spaces.id", ondelete="CASCADE"), nullable=False)

    space = relationship("Space", back_populates="labels")
    threads = relationship("ThreadLabel", back_populates="label")