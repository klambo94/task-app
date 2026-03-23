from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models import User


def get_current_user(db: Session = Depends(get_db)) -> User:
    user = db.query(User).filter(User.deletedAt.is_(None)).first()
    if user is None:
        raise RuntimeError(
            "No users found in the database. "
            "Seed a user before testing authenticated routes."
        )
    return user