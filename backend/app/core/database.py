from typing import Any, Generator

from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker, Session

from app.core.config import settings
from app.models import User


class Base(DeclarativeBase):
    pass


engine = create_engine(settings.database_url)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(db: Session = Depends(get_db)) -> User:
    """
    Stub auth dependency. Returns a hardcoded user for development.
    Replace with real Kinde JWT verification when auth is wired up.
    """
    user = db.query(User).filter(User.deletedAt.is_(None)).first()
    if user is None:
        raise RuntimeError(
            "No users found in the database. "
            "Seed a user before testing authenticated routes."
        )
    return user
