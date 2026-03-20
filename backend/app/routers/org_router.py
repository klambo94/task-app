from fastapi import APIRouter, Depends, Query, HTTPException
from slugify import slugify
from sqlalchemy.orm import Session

from app.core.database import get_db, get_current_user
from app.models import User
from app.repositories import OrgRepository, OrgMemberRepository
from app.schemas import OrgCreate, OrgRead, OrgUpdate
from app.schemas.response_schema import MessageResponse, DataResponse

router = APIRouter(prefix="/orgs", tags=["orgs"])


def get_org_repo(db: Session = Depends(get_db)) -> OrgRepository:
    return OrgRepository(db)


def get_member_repo(db: Session = Depends(get_db)) -> OrgMemberRepository:
    return OrgMemberRepository(db)


@router.get("", response_model=DataResponse[OrgRepository])
def list_orgs(
        cursor: str | None = Query(default=None),
        limit: int = Query(default=20, ge=1, le=100),
        repo: OrgRepository = Depends(get_org_repo),
        _: User = Depends(get_current_user),
):
    return DataResponse(data=repo.list(cursor=cursor, limit=limit))

@router.post("}", response_model=DataResponse[OrgRepository])
def create_org(
        body: OrgCreate,
        repo: OrgRepository = Depends(get_org_repo),
        member_repo: OrgMemberRepository = Depends(get_member_repo),
        current_user: User = Depends(get_current_user),
):
    slug = slugify(body.slug or body.name)
    if repo.get_by_slug(slug):
        raise HTTPException(status_code=409, detail="Org already exists")

    org = repo.create(name=body.name, slug=slug)
    member_repo.create(org_id=org.id, user_id=current_user.id)

    return DataResponse(data=org)

@router.get("/{org_id}", response_model=DataResponse[OrgRead])
def get_org(
        org_id: str,
        repo: OrgRepository = Depends(get_org_repo),
        _ : User = Depends(get_current_user),
):
    org = repo.get_by_id(org_id)
    if not org:
        raise HTTPException(status_code=404, detail="Org not found")
    return DataResponse(data=org)

@router.patch("/{org_id}", response_model=DataResponse[OrgRead])
def update_org(
        org_id: str,
        body: OrgUpdate,
        repo: OrgRepository = Depends(get_org_repo),
        _: User = Depends(get_current_user),
):
    org = repo.get_by_id(org_id)
    if not org:
        raise HTTPException(status_code=404, detail="Org not found")

    if body.slug is not None:
        slug = slugify(body.slug)
        existing = repo.get_by_slug(slug)
        if existing and existing.id != org_id:
            raise HTTPException(status_code=409, detail="An org with this slug already exists")

        body = body.model_copy(update={"slug": slug})

    org = repo.update(org, name=body.name, slug=body.slug)
    return DataResponse(data=org)

@router.delete("/{org_id}", response_model=MessageResponse)
def delete_org(
    org_id: str,
    repo: OrgRepository = Depends(get_org_repo),
    _: User = Depends(get_current_user),
):
    org = repo.get_by_id(org_id)
    if org is None:
        raise HTTPException(status_code=404, detail="Org not found")
    repo.soft_delete(org)
    return MessageResponse(message="Org deleted successfully")