import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

DB_FILE_PATH = 'sqlite:///./task-app.db'
engine = create_engine(DB_FILE_PATH, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit= False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass