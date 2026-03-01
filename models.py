import datetime

from enums import Status
from database import Base, engine
from sqlalchemy import Column, Integer, String, DateTime, Enum as SAEnum



class Task(Base):
    __tablename__ = "tasks"

    id= Column(Integer, primary_key=True, index=True)
    name= Column(String, nullable=False)
    description= Column(String, nullable=False)
    status= Column(SAEnum(Status), default=Status.OPEN)
    created_at= Column(DateTime(), default=lambda: datetime.datetime.now(datetime.UTC))
    updated_at= Column(DateTime(), default=lambda: datetime.datetime.now(datetime.UTC))





