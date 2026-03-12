import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from repositories import status_repository, access_repository
from schemas import SprintStatusCreate
from schemas.status_schema import StatusCreate, StatusUpdate, StatusReorder, StatusResponse
from schemas.shared import DataResponse

log = logging.getLogger(__name__)
router = APIRouter(prefix="/api", tags=["status"])


@router.get("/spaces/{space_id}/status", response_model=DataResponse[list[StatusResponse]])
def get_statuses(space_id: str,
                 user_id: str,# Temp, once auth is hooked up use:  current_user = Depends(current_user)
                 session: Session = Depends(get_db)):
    if not access_repository.can_access_space(user_id, space_id, session):
        raise HTTPException(status_code=403, detail="Access denied")

    statuses = status_repository.get_by_space(space_id, session)
    return DataResponse(data=statuses)


@router.post("/spaces/{space_id}/status", response_model=DataResponse[StatusResponse])
def create_status(
    space_id: str,
    status_in: StatusCreate,
    user_id: str, # Temp, once auth is hooked up use:  current_user = Depends(current_user)
    session: Session = Depends(get_db)
):
    if not access_repository.can_admin_space(user_id, space_id, session):
        raise HTTPException(status_code=403, detail="Admin access required")

    status_in = StatusCreate(**status_in.model_dump(exclude={"spaceId"}), spaceId=space_id)
    status = status_repository.create(status_in, session)
    return DataResponse(data=status)


@router.post("/spaces/{space_id}/status/reorder")
def reorder_statuses(
    space_id: str,
    reorders: list[StatusReorder],
    user_id: str,# Temp, once auth is hooked up use:  current_user = Depends(current_user)
    session: Session = Depends(get_db)
):
    if not access_repository.can_admin_space(user_id, space_id, session):
        raise HTTPException(status_code=403, detail="Admin access required")

    status_repository.reorder(reorders, session)
    return {"message": "Statuses reordered"}


@router.patch("/status/{status_id}", response_model=DataResponse[StatusResponse])
def update_status(
    status_id: str,
    status_in: StatusUpdate,
    session: Session = Depends(get_db)
):
    status = status_repository.update(status_id, status_in, session)
    if not status:
        raise HTTPException(status_code=404, detail="Status not found")
    return DataResponse(data=status)


@router.delete("/status/{status_id}")
def delete_status(status_id: str, session: Session = Depends(get_db)):
    success = status_repository.delete(status_id, session)
    if not success:
        raise HTTPException(status_code=404, detail="Status not found")
    return {"message": "Status deleted"}