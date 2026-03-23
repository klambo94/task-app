from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_current_user
from app.models import User
from app.repositories import LabelRepository, SpaceRepository
from app.schemas import LabelPage, LabelRead, LabelCreate, LabelUpdate
from app.schemas.response_schema import DataResponse, MessageResponse

spaces_label_router = APIRouter(prefix="/spaces", tags=["Labels"])
label_router = APIRouter(prefix="/labels", tags=["Labels"])

@spaces_label_router.get("/{space_id}/labels", response_model=DataResponse[LabelPage])
def get_space_labels(
        space_id: str,
        cursor: str | None = Query(default=None),
        limit: int = Query(default=20, ge=1, le=1000),
        db: Session = Depends(get_db),
        _: User = Depends(get_current_user)
):
    space_repo = SpaceRepository(db=db)
    label_repo = LabelRepository(db=db)

    space = space_repo.get_by_id(space_id)
    if not space:
        raise HTTPException(status_code=404, detail="Space not found")

    return DataResponse(data=label_repo.list_by_space(space_id=space.id, cursor=cursor, limit=limit))

@spaces_label_router.post("/{space_id}/labels", response_model=DataResponse[LabelRead])
def create_label(
        space_id: str,
        label: LabelCreate,
        db: Session = Depends(get_db),
        _: User = Depends(get_current_user)
):
    space_repo = SpaceRepository(db=db)
    label_repo = LabelRepository(db=db)

    space = space_repo.get_by_id(space_id=space_id)
    if not space:
        raise HTTPException(status_code=404, detail="Space not found")

    existing_label = label_repo.get_by_name(name=label.name)
    if existing_label:
        raise HTTPException(status_code=400, detail="Label already exists")

    label = label_repo.create(space_id=space_id, name=label.name)
    db.commit()
    return DataResponse(data=label)


@label_router.get("/{label_id}", response_model=DataResponse[LabelRead])
def get_label(
        label_id: str,
        db: Session = Depends(get_db),
        _: User = Depends(get_current_user)
):
    label_repo = LabelRepository(db=db)

    label = label_repo.get_by_id(label_id=label_id)
    if not label:
        raise HTTPException(status_code=404, detail="Label not found")
    return DataResponse(data=label)

@label_router.patch("/{label_id}", response_model=DataResponse[LabelRead])
def update_label(
        label_id: str,
        body: LabelUpdate,
        db: Session = Depends(get_db),
        _: User = Depends(get_current_user)
):
    label_repo = LabelRepository(db=db)

    label = label_repo.get_by_id(label_id=label_id)
    if not label:
        raise HTTPException(status_code=404, detail="Label not found")

    if body.name is not None:
        label.name = body.name
    if body.color is not None:
        label.color = body.color

    label = label_repo.update(label, name=label.name, color=label.color)
    db.commit()
    return DataResponse(data=label)


@label_router.delete("/{label_id}", response_model=MessageResponse)
def delete_label(
        label_id: str,
        db: Session = Depends(get_db),
        _: User = Depends(get_current_user)
):
    label_repo = LabelRepository(db=db)

    label = label_repo.get_by_id(label_id)
    if not label:
        raise HTTPException(status_code=404, detail="Label not found")

    try:
        label_repo.soft_delete(label)
    except IntegrityError:
        raise HTTPException(status_code=409, detail="Status is in use and cannot be deleted")

    db.commit()
    return MessageResponse(message="Label deleted successfully")