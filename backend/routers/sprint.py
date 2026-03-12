import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from dependencies.auth import get_current_user
from repositories import sprint_repository, access_repository
from schemas.sprint_schema import (
    SprintCreate, SprintUpdate, SprintResponse,
    SprintStatusCreate, SprintStatusUpdate, SprintStatusResponse,
)
from schemas.shared import DataResponse

log = logging.getLogger(__name__)
router = APIRouter(prefix="/api", tags=["sprints"])


# Sprints  -----------------------------------------------------------------------------

@router.post("/sprints", response_model=DataResponse[SprintResponse])
def create_sprint(
    sprint_in: SprintCreate,
    current_user=Depends(get_current_user),
    session: Session = Depends(get_db)
):
    if not access_repository.can_access_space(current_user.id, sprint_in.spaceId, session):
        raise HTTPException(status_code=403, detail="Access denied")

    sprint = sprint_repository.create(sprint_in, session)
    return DataResponse(data=sprint)


@router.get("/spaces/{space_id}/sprints", response_model=DataResponse[list[SprintResponse]])
def get_sprints(
    space_id: str,
    current_user=Depends(get_current_user),
    session: Session = Depends(get_db)
):
    if not access_repository.can_access_space(current_user.id, space_id, session):
        raise HTTPException(status_code=403, detail="Access denied")

    sprints = sprint_repository.get_by_space(space_id, session)
    return DataResponse(data=sprints)


@router.get("/spaces/{space_id}/sprints/active", response_model=DataResponse[SprintResponse])
def get_active_sprint(
    space_id: str,
    current_user=Depends(get_current_user),
    session: Session = Depends(get_db)
):
    if not access_repository.can_access_space(current_user.id, space_id, session):
        raise HTTPException(status_code=403, detail="Access denied")

    sprint = sprint_repository.get_active(space_id, session)
    if not sprint:
        raise HTTPException(status_code=404, detail="No active sprint found")
    return DataResponse(data=sprint)


@router.get("/sprints/{sprint_id}", response_model=DataResponse[SprintResponse])
def get_sprint(
    sprint_id: str,
    current_user=Depends(get_current_user),
    session: Session = Depends(get_db)
):
    if not access_repository.can_access_sprint(current_user.id, sprint_id, session):
        raise HTTPException(status_code=403, detail="Access denied")

    sprint = sprint_repository.get_by_id(sprint_id, session)
    if not sprint:
        raise HTTPException(status_code=404, detail="Sprint not found")
    return DataResponse(data=sprint)


@router.patch("/sprints/{sprint_id}", response_model=DataResponse[SprintResponse])
def update_sprint(
    sprint_id: str,
    sprint_in: SprintUpdate,
    current_user=Depends(get_current_user),
    session: Session = Depends(get_db)
):
    if not access_repository.can_access_sprint(current_user.id, sprint_id, session):
        raise HTTPException(status_code=403, detail="Access denied")

    sprint = sprint_repository.update(sprint_id, sprint_in, session)
    if not sprint:
        raise HTTPException(status_code=404, detail="Sprint not found")
    return DataResponse(data=sprint)


@router.delete("/sprints/{sprint_id}")
def delete_sprint(
    sprint_id: str,
    current_user=Depends(get_current_user),
    session: Session = Depends(get_db)
):
    if not access_repository.can_access_sprint(current_user.id, sprint_id, session):
        raise HTTPException(status_code=403, detail="Access denied")

    success = sprint_repository.delete(sprint_id, session)
    if not success:
        raise HTTPException(status_code=404, detail="Sprint not found")
    return {"message": "Sprint deleted"}


# Sprint Statuses ───────────────────────────────────────────────────────────

@router.get("/spaces/{space_id}/sprint-status", response_model=DataResponse[list[SprintStatusResponse]])
def get_sprint_statuses(
    space_id: str,
    current_user=Depends(get_current_user),
    session: Session = Depends(get_db)
):
    if not access_repository.can_access_space(current_user.id, space_id, session):
        raise HTTPException(status_code=403, detail="Access denied")

    statuses = sprint_repository.get_sprint_statuses(space_id, session)
    return DataResponse(data=statuses)


@router.post("/spaces/{space_id}/sprint-status", response_model=DataResponse[SprintStatusResponse])
def create_sprint_status(
    space_id: str,
    status_in: SprintStatusCreate,
    current_user=Depends(get_current_user),
    session: Session = Depends(get_db)
):
    if not access_repository.can_admin_space(current_user.id, space_id, session):
        raise HTTPException(status_code=403, detail="Admin access required")

    status_in = SprintStatusCreate(**status_in.model_dump(exclude={"spaceId"}), spaceId=space_id)
    status = sprint_repository.create_sprint_status(status_in, session)
    return DataResponse(data=status)


@router.patch("/sprint-status/{status_id}", response_model=DataResponse[SprintStatusResponse])
def update_sprint_status(
    status_id: str,
    status_in: SprintStatusUpdate,
    current_user=Depends(get_current_user),
    session: Session = Depends(get_db)
):
    status = sprint_repository.update_sprint_status(status_id, status_in, session)
    if not status:
        raise HTTPException(status_code=404, detail="Sprint status not found")
    return DataResponse(data=status)


@router.delete("/sprint-status/{status_id}")
def delete_sprint_status(
    status_id: str,
    current_user=Depends(get_current_user),
    session: Session = Depends(get_db)
):
    success = sprint_repository.delete_sprint_status(status_id, session)
    if not success:
        raise HTTPException(status_code=404, detail="Sprint status not found")
    return {"message": "Sprint status deleted"}