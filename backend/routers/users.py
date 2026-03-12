import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from dependencies.auth import get_current_user
from repositories import user_repository
from schemas.user_schema import UserResponse, UserUpdate
from schemas.shared import DataResponse

log = logging.getLogger(__name__)
router = APIRouter(prefix="/api/users", tags=["users"])


@router.get("/me", response_model=DataResponse[UserResponse])
def get_me(
    current_user=Depends(get_current_user),
    session: Session = Depends(get_db)
):
    user = user_repository.get_by_id(current_user.id, session)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return DataResponse(data=user)


@router.get("/{user_id}", response_model=DataResponse[UserResponse])
def get_user(
    user_id: str,
    current_user=Depends(get_current_user),
    session: Session = Depends(get_db)
):
    user = user_repository.get_by_id(user_id, session)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return DataResponse(data=user)


@router.patch("/me", response_model=DataResponse[UserResponse])
def update_me(
    user_in: UserUpdate,
    current_user=Depends(get_current_user),
    session: Session = Depends(get_db)
):
    user = user_repository.update(current_user.id, user_in, session)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return DataResponse(data=user)


@router.delete("/me")
def delete_me(
    current_user=Depends(get_current_user),
    session: Session = Depends(get_db)
):
    success = user_repository.delete(current_user.id, session)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted"}