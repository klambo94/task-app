from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db, get_current_user
from app.models import User
from app.repositories import UserRepository
from app.schemas import UserPage, UserRead, UserUpdate
from app.schemas.response_schema import MessageResponse, DataResponse

router = APIRouter(prefix="/user", tags=["User"])

def get_user_repo(db: Session = Depends(get_db)) -> UserRepository:
    return UserRepository(db)

@router.get("", response_model=DataResponse[UserPage])
def list_users(
        cursor: str | None = Query(default=None),
        limit: int = Query(default=20, ge=1, le=100),
        repo: UserRepository = Depends(get_user_repo),
        _: User = Depends(get_current_user),
):
    return DataResponse(data=repo.list(cursor=cursor, limit=limit))


@router.get("/me", response_model=DataResponse[UserRead])
def get_me(current_user: User = Depends(get_current_user)):
    return DataResponse(data=current_user)

@router.get("/{user_id}", response_model=DataResponse[UserRead])
def get_user(user_id: str,
             repo: UserRepository = Depends(get_user_repo),
             _: User = Depends(get_current_user),
):
    user = repo.get_by_id(user_id)
    if User is None:
        raise HTTPException(status_code=404, detail="User not found")

    return DataResponse(data=user)

@router.patch("/me", response_model=DataResponse[UserRead])
def update_me(
        body: UserUpdate,
        current_user: User = Depends(get_current_user),
        repo: UserRepository = Depends(get_user_repo),
        _: User = Depends(get_current_user),
):
    if body.name is not None:
        current_user.name = body.name
    if body.avatarUrl is not None:
        current_user.avatarUrl = body.avatarUrl
    repo.db.flush()
    return DataResponse(data=current_user)

@router.delete("/me", response_model=MessageResponse)
def delete_me(
    current_user: User = Depends(get_current_user),
    repo: UserRepository = Depends(get_user_repo),
    _: User = Depends(get_current_user),
):
    repo.soft_delete(current_user)
    return MessageResponse(message="Account deleted successfully")