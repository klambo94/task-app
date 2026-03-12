import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from dependencies.auth import get_current_user
from repositories import space_repository, access_repository
from schemas.space_schema import SpaceCreate, SpaceUpdate, SpaceResponse
from schemas.shared import DataResponse

log = logging.getLogger(__name__)
router = APIRouter(prefix="/api/spaces", tags=["spaces"])


@router.get("/", response_model=DataResponse[list[SpaceResponse]])
def get_spaces(
    current_user=Depends(get_current_user),
    org_id: str | None = None,
    session: Session = Depends(get_db)
):
    if org_id:
        if not access_repository.is_org_member(current_user.id, org_id, session):
            raise HTTPException(status_code=403, detail="Access denied")
        spaces = space_repository.get_by_org(org_id, session)
    else:
        spaces = space_repository.get_by_user(current_user.id, session)
    return DataResponse(data=spaces)


@router.post("/", response_model=DataResponse[SpaceResponse])
def create_space(
    space_in: SpaceCreate,
    current_user=Depends(get_current_user),
    session: Session = Depends(get_db)
):
    if space_in.organizationId:
        if not access_repository.is_org_member(current_user.id, space_in.organizationId, session):
            raise HTTPException(status_code=403, detail="Access denied")

    space_in = SpaceCreate(
        name=space_in.name,
        ownerId=current_user.id,
        organizationId=space_in.organizationId,
        description=space_in.description,
        visibility=space_in.visibility,
    )
    space = space_repository.create(space_in=space_in, session=session)
    return DataResponse(data=space)


@router.get("/{space_id}", response_model=DataResponse[SpaceResponse])
def get_space(
    space_id: str,
    current_user=Depends(get_current_user),
    session: Session = Depends(get_db)
):
    if not access_repository.can_access_space(current_user.id, space_id, session):
        raise HTTPException(status_code=403, detail="Access denied")

    space = space_repository.get_by_id(space_id, session)
    if not space:
        raise HTTPException(status_code=404, detail="Space not found")
    return DataResponse(data=space)


@router.patch("/{space_id}", response_model=DataResponse[SpaceResponse])
def update_space(
    space_id: str,
    space_in: SpaceUpdate,
    current_user=Depends(get_current_user),
    session: Session = Depends(get_db)
):
    if not access_repository.can_admin_space(current_user.id, space_id, session):
        raise HTTPException(status_code=403, detail="Admin access required")

    space = space_repository.update(space_id, space_in, session)
    if not space:
        raise HTTPException(status_code=404, detail="Space not found")
    return DataResponse(data=space)


@router.delete("/{space_id}")
def delete_space(
    space_id: str,
    current_user=Depends(get_current_user),
    session: Session = Depends(get_db)
):
    if not access_repository.can_admin_space(current_user.id, space_id, session):
        raise HTTPException(status_code=403, detail="Admin access required")

    success = space_repository.delete(space_id, session)
    if not success:
        raise HTTPException(status_code=404, detail="Space not found")
    return {"message": "Space deleted"}