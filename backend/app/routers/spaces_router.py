from fastapi import APIRouter, Depends, HTTPException, Query
from slugify import slugify
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from app.core.database import get_db
from app.models import User
from app.repositories import SpaceRepository, OrgRepository
from app.schemas import SpaceRead, SpacePage, SpaceCreate
from app.schemas.response_schema import DataResponse, MessageResponse

spaces_router = APIRouter(prefix="/space", tags=["Spaces"])
org_spaces_router = APIRouter(prefix="/orgs", tags=["Spaces"])

def get_space_repo(db: Session = Depends(get_db)) -> SpaceRepository:
    return SpaceRepository(db)

@org_spaces_router.post("/{org_id}/spaces", response_model=DataResponse[SpaceRead])
def create_space(
        org_id: str,
        body: SpaceCreate,
        db: Session = Depends(get_db),
        _: User = Depends(get_current_user),
):
    org_repo = OrgRepository(db)
    space_repo = SpaceRepository(db)

    if not org_repo.get_by_id(org_id):
        raise HTTPException(status_code=404, detail="Org not found")

    slug = slugify(body.slug or body.name)
    if space_repo.get_by_slug(org_id=org_id, slug=slug):
        raise HTTPException(status_code=409, detail="Space with this slug already exists in org")

    space = space_repo.create(org_id=org_id, name=body.name, slug=slug)
    db.commit()

    return DataResponse(data=space)


@org_spaces_router.get("/{org_id}/spaces", response_model=DataResponse[SpacePage])
def list_spaces(
        org_id: str,
        cursor: str | None = Query(default=None),
        limit: int = Query(default=20, ge=1, le=100),
        db: Session = Depends(get_db),
        _: User = Depends(get_current_user),
):
    org_repo = OrgRepository(db)
    space_repo = SpaceRepository(db)

    if not org_repo.get_by_id(org_id):
        raise HTTPException(status_code=404, detail="Org not found")

    return DataResponse(data=space_repo.list_by_org(org_id=org_id, cursor=cursor, limit=limit))



@spaces_router.get("/{space_id}", response_model=DataResponse[SpaceRead])
def get_space(
        space_id: str,
        repo: SpaceRepository = Depends(get_space_repo),
        _: User = Depends(get_current_user),
):
    space = repo.get_by_id(space_id)

    if not space:
        raise HTTPException(status_code=404, detail="Space not found")
    return DataResponse(data=space)

@spaces_router.patch("/{space_id}", response_model=DataResponse[SpaceRead])
def update_space(
        space_id: str,
        body: SpaceCreate,
        repo: SpaceRepository = Depends(get_space_repo),
        _: User = Depends(get_current_user),
):
    space = repo.get_by_id(space_id)
    if not space:
        raise HTTPException(status_code=404, detail="Space not found")

    if body.slug is not None:
        slug = slugify(body.slug or body.name)
        existing = repo.get_by_slug(org_id=space.orgId, slug=slug)
        if existing and existing.id != space.id:
            raise HTTPException(status_code=409, detail="Space with this slug already exists in org")
        body = body.model_copy(update={"slug": slug})

    space = repo.update(space, name=body.name, slug=body.slug)
    return DataResponse(data=space)


@spaces_router.delete("/{space_id}", response_model=DataResponse[SpaceRead])
def delete_space(
        space_id: str,
        repo: SpaceRepository = Depends(get_space_repo),
        _: User = Depends(get_current_user),
):
    space = repo.get_by_id(space_id)
    if not space:
        raise HTTPException(status_code=404, detail="Space not found")
    repo.soft_delete(space)
    return MessageResponse(message="Space successfully deleted")