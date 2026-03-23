from sqlite3 import IntegrityError

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_current_user
from app.models import User
from app.repositories import StatusRepository, SpaceRepository
from app.schemas import StatusRead, StatusCreate, StatusPage, StatusUpdate
from app.schemas.response_schema import DataResponse, MessageResponse

spaces_status_router = APIRouter(prefix="/spaces", tags=["Status"])
status_router = APIRouter(prefix="/statuses", tags=["Status"])


def get_status_repo(db: Session = Depends(get_db)) -> StatusRepository:
    return StatusRepository(db=db)

def get_space_repo(db: Session = Depends(get_db)) -> SpaceRepository:
    return SpaceRepository(db=db)

@spaces_status_router.get("/{space_id}/statuses", response_model=DataResponse[StatusPage])
def list_statuses(
        space_id: str,
        cursor: str | None = Query(default=None),
        limit: int = Query(default=20, ge=1, le=100),
        db: Session = Depends(get_db),
        _: User = Depends(get_current_user),
):
    status_repo = StatusRepository(db=db)
    space_repo = SpaceRepository(db=db)

    space = space_repo.get_by_id(space_id)
    if not space:
        raise HTTPException(status_code=404, detail="Space not found")


    return DataResponse(data=status_repo.list_by_space(space_id=space_id, cursor=cursor, limit=limit))

@spaces_status_router.post("/{space_id}/statuses", response_model=DataResponse[StatusRead])
def create_status(
        space_id: str,
        body: StatusCreate,
        db: Session = Depends(get_db),
        _: User = Depends(get_current_user),
):
    status_repo = StatusRepository(db=db)
    space_repo = SpaceRepository(db=db)

    space = space_repo.get_by_id(space_id)
    if not space:
        raise HTTPException(status_code=404, detail="Space not found")

    status = status_repo.get_by_name(name=body.name)
    if status:
        raise HTTPException(status_code=400, detail="Status already exists")

    status = status_repo.create(space_id=space_id, name=body.name, color=body.color,
                                category=body.category, sort_order=body.sortOrder)
    db.commit()

    return DataResponse(data=status)


@status_router.get("/{status_id}", response_model=DataResponse[StatusRead])
def get_status(
        status_id: str,
        repo: StatusRepository = Depends(get_status_repo),
        _: User = Depends(get_current_user),
):
    status = repo.get_by_id(status_id)
    if not status:
        raise HTTPException(status_code=404, detail="Status not found")
    return DataResponse(data=status)

@status_router.patch("/{status_id}", response_model=DataResponse[StatusRead])
def update_status(
        status_id: str,
        body: StatusUpdate,
        db: Session = Depends(get_db),
        _: User = Depends(get_current_user),
):

    repo = StatusRepository(db=db)

    status = repo.get_by_id(status_id)
    if not status:
        raise HTTPException(status_code=404, detail="Status not found")

    if body.name is not None:
        status.name = body.name

    if body.color is not None:
        status.color = body.color
    if body.category is not None:
        status.category = body.category
    if body.sortOrder is not None:
        status.sort_order = body.sortOrder
    status = repo.update(status)
    db.commit()

    return DataResponse(data=status)


@status_router.delete("/{status_id}", response_model=MessageResponse)
def delete_status(
        status_id: str,
        repo: StatusRepository = Depends(get_status_repo),
        _: User = Depends(get_current_user),
):

    status = repo.get_by_id(status_id)
    if not status:
        raise HTTPException(status_code=404, detail="Status not found")

    try:
        repo.soft_delete(status)
    except IntegrityError:
        raise HTTPException(status_code=409, detail="Status is in use and cannot be deleted")
    return MessageResponse(message="Status deleted")