import logging

from fastapi import Depends
from pydantic import EmailStr
from sqlalchemy.orm import Session

from database import SessionLocal
from models import User
from schemas.user_schema import UserUpdate, UserCreate

log = logging.getLogger(__name__)

def create(user_in: UserCreate, session: Session):
    from utils import generate_id
    user = User(
        id=generate_id(),
        email=user_in.email,
        name=user_in.name,
        image=user_in.image,
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user
def get_by_id(user_id: str, session: Session):
    log.debug(f"get_user_by_id: {user_id}")
    return session.query(User).filter(User.id == user_id).first()

def get_by_email(email: str, session: Session = Depends(SessionLocal)):
    log.debug(f"get_user_by_email: {email}")
    return session.query(User).filter(User.email == email).first()

def update(user_id: str, user_in: UserUpdate, session: Session):
    user = get_by_id(user_id, session)

    if not user:
        log.info("User not found")
        return None

    for field, value in user_in.model_dump(exclude_unset=True).items():
        setattr(user, field, value)

    session.commit()
    session.refresh(user)
    return user


def delete(user_id: int, session: Session = Depends(SessionLocal)):
    log.debug(f"delete_user: {user_id}")
    user = get_by_id(user_id, session)

    if not user:
        return False

    session.delete(user)
    session.commit()
    log.info("User deleted!")
    return True