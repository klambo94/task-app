
from google.auth import jwt

from settings import NEXTAUTH_SECRET

import jwt
from fastapi import Header, HTTPException, Depends
from sqlalchemy.orm import Session

from database import get_db
from repositories import user_repository



def get_current_user(
    authorization: str = Header(...),
    session: Session = Depends(get_db)
):
    try:
        token = authorization.replace("Bearer ", "")
        payload = jwt.decode(token, NEXTAUTH_SECRET, algorithms=["HS256"])
        email: str = payload.get("email")
        if not email:
            raise HTTPException(status_code=401, detail="Invalid token payload")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = user_repository.get_by_email(email, session)
    if not user:
        # Auto-create user on first Google login
        from schemas.user_schema import UserCreate
        user = user_repository.create(
            UserCreate(email=email, name=payload.get("name")),
            session
        )

    return user