import os
from fastapi import Header, HTTPException, Depends
from sqlalchemy.orm import Session

from database import get_db
from repositories import user_repository
from settings import INTERNAL_SECRET


def get_current_user(
        x_internal_secret: str = Header(...),
        x_user_id: str = Header(...),
        session: Session = Depends(get_db)
):
    if not INTERNAL_SECRET or x_internal_secret != INTERNAL_SECRET:
        raise HTTPException(status_code=401, detail="Unauthorized")

    user = user_repository.get_by_id(x_user_id, session)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user