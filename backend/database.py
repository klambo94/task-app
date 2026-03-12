import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from settings import DATABASE_URL

engine = create_engine(url=DATABASE_URL)
SessionLocal = sessionmaker(autocommit= False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass


def get_db():
    print("\n--- get_db called ---")

    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
