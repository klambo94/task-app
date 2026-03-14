import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from dependencies.auth import get_current_user
from repositories import label_repository, access_repository
from schemas.label_schema import LabelCreate, LabelUpdate, LabelResponse
from schemas.shared import DataResponse

log = logging.getLogger(__name__)
router = APIRouter(prefix="/api", tags=["labels"])


@router.get("/spaces/{space_id}/labels", response_model=DataResponse[list[LabelResponse]])
def get_labels(
    space_id: str,
    current_user=Depends(get_current_user),
    session: Session = Depends(get_db)
):
    if not access_repository.can_access_space(current_user.id, space_id, session):
        raise HTTPException(status_code=403, detail="Access denied")

    labels = label_repository.get_by_space(space_id, session)
    return DataResponse(data=labels)


@router.post("/labels", response_model=DataResponse[LabelResponse])
def create_label(
    label_in: LabelCreate,
    current_user=Depends(get_current_user),
    session: Session = Depends(get_db)
):
    if not access_repository.can_access_space(current_user.id, label_in.spaceId, session):
        raise HTTPException(status_code=403, detail="Access denied")

    label = label_repository.create(label_in, session)
    return DataResponse(data=label)


@router.patch("/labels/{label_id}", response_model=DataResponse[LabelResponse])
def update_label(
    label_id: str,
    label_in: LabelUpdate,
    current_user=Depends(get_current_user),
    session: Session = Depends(get_db)
):
    label = label_repository.get_by_id(label_id, session)
    if not label:
        raise HTTPException(status_code=404, detail="Label not found")
    if not access_repository.can_access_space(current_user.id, label.spaceId, session):
        raise HTTPException(status_code=403, detail="Access denied")

    updated = label_repository.update(label_id, label_in, session)
    return DataResponse(data=updated)

@router.delete("/labels/{label_id}")
def delete_label(
    label_id: str,
    current_user=Depends(get_current_user),  # ← remove space_id param
    session: Session = Depends(get_db)
):
    label = label_repository.get_by_id(label_id, session)
    if not label:
        raise HTTPException(status_code=404, detail="Label not found")
    if not access_repository.can_access_space(current_user.id, label.spaceId, session):
        raise HTTPException(status_code=403, detail="Access denied")

    label_repository.delete(label_id, session)
    return {"message": "Label deleted"}