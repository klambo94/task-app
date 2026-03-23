from typing import Any

from fastapi import APIRouter, Depends, Query, HTTPException
from slugify import slugify
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_current_user
from app.models import User, OrgMember
from app.repositories import OrgRepository, OrgMemberRepository
from app.schemas import OrgCreate, OrgRead, OrgUpdate, OrgMemberPage, OrgPage
from app.schemas.response_schema import MessageResponse, DataResponse

router = APIRouter(prefix="/orgs", tags=["Orgs"])


def get_org_repo(db: Session = Depends(get_db)) -> OrgRepository:
    return OrgRepository(db)


def get_member_repo(db: Session = Depends(get_db)) -> OrgMemberRepository:
    return OrgMemberRepository(db)


@router.get("", response_model=DataResponse[OrgPage])
def list_orgs(
        cursor: str | None = Query(default=None),
        limit: int = Query(default=20, ge=1, le=100),
        repo: OrgRepository = Depends(get_org_repo),
        _: User = Depends(get_current_user),
):
    return DataResponse(data=repo.list(cursor=cursor, limit=limit))

@router.post("", response_model=DataResponse[OrgRead])
def create_org(
        body: OrgCreate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user),
):
    repo = OrgRepository(db)
    member_repo = OrgMemberRepository(db)

    slug = slugify(body.slug or body.name)
    if repo.get_by_slug(slug):
        raise HTTPException(status_code=409, detail="Org already exists")

    org = repo.create(name=body.name, slug=slug)
    member_repo.create(org_id=org.id, user_id=current_user.id)
    db.commit()

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

@router.get("/{org_id}/members", response_model=DataResponse[OrgMemberPage])
def get_org_members(
    org_id: str,
    cursor: str | None = Query(default=None),
    limit: int = Query(default=20, ge=1, le=100),
    repo: OrgMemberRepository = Depends(get_member_repo),
    _: User = Depends(get_current_user),
):
    return DataResponse(data=repo.list_by_org(org_id, cursor=cursor, limit=limit))

@router.delete("/{org_id}/members/{member_id}", response_model=MessageResponse)
def delete_org_member(
        org_id: str,
        member_id: str,
        repo: OrgMemberRepository = Depends(get_member_repo),
        _: User = Depends(get_current_user),
):
    org_mem: Any | None = repo.db.query(OrgMember).filter(
        OrgMember.orgId == org_id,
        OrgMember.id == member_id,
        OrgMember.deletedAt.is_(None),
    ).first()
    if org_mem is None:
        raise HTTPException(status_code=404, detail="Org Member not found")

    repo.soft_delete(org_mem)
    return MessageResponse(message="Member deleted successfully")

