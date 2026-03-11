from sqlalchemy.orm import relationship

from enums import Status
from database import Base
from sqlalchemy import Column, Integer, String, DateTime, Enum as SAEnum, Boolean, func, ForeignKey

class Task(Base):
    __tablename__ = "tasks"

    id= Column(Integer, primary_key=True, index=True)
    name= Column(String, nullable=False)
    description= Column(String, nullable=False)
    status= Column(SAEnum(Status), default=Status.OPEN)
    created_at= Column(DateTime(), server_default=func.now())
    updated_at= Column(DateTime(), server_default=func.now())
    board_id = Column(Integer, ForeignKey("boards.id"), nullable=False)

    board = relationship("Board", back_populates="tasks")





