
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_current_user
from app.models import User
from app.models.enums import InvitationStatus
from app.repositories import InvitationRepository, OrgRepository
from app.schemas import InvitationRead, InvitationCreate, InvitationUpdate, InvitationPage
from app.schemas.response_schema import DataResponse, MessageResponse

org_invitation_router = APIRouter(prefix="/orgs", tags=["Invitations"])
invitation_router = APIRouter(prefix="/invitations", tags=["Invitations"])


@org_invitation_router.get("/{org_id}/invitations", response_model=DataResponse[InvitationPage])
def list_invitations(
    org_id: str,
    status: InvitationStatus | None = Query(default=None),
    cursor: str | None = Query(default=None),
    limit: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    org_repo = OrgRepository(db)
    invitation_repo = InvitationRepository(db)

    if not org_repo.get_by_id(org_id):
        raise HTTPException(status_code=404, detail="Org not found")

    return DataResponse(data=invitation_repo.list_by_org(org_id=org_id, status=status, cursor=cursor, limit=limit))


@org_invitation_router.post("/{org_id}/invitations", response_model=DataResponse[InvitationRead])
def create_invitation(
    org_id: str,
    body: InvitationCreate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    org_repo = OrgRepository(db)
    invitation_repo = InvitationRepository(db)

    if not org_repo.get_by_id(org_id):
        raise HTTPException(status_code=404, detail="Org not found")

    existing = invitation_repo.get_pending_by_email(org_id=org_id, email=body.email)
    if existing:
        raise HTTPException(status_code=409, detail="A pending invitation already exists for this email")

    invitation = invitation_repo.create(
        org_id=org_id,
        email=body.email,
        token_hash=body.tokenHash,
        expires_at=body.expiresAt,
    )
    db.commit()
    return DataResponse(data=invitation)


@org_invitation_router.get("/{org_id}/invitations/{invitation_id}", response_model=DataResponse[InvitationRead])
def get_invitation(
    org_id: str,
    invitation_id: str,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    invitation_repo = InvitationRepository(db)
    invitation = invitation_repo.get_by_id(invitation_id)
    if not invitation or invitation.orgId != org_id:
        raise HTTPException(status_code=404, detail="Invitation not found")
    return DataResponse(data=invitation)


@org_invitation_router.patch("/{org_id}/invitations/{invitation_id}", response_model=DataResponse[InvitationRead])
def update_invitation(
    org_id: str,
    invitation_id: str,
    body: InvitationUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    invitation_repo = InvitationRepository(db)
    invitation = invitation_repo.get_by_id(invitation_id)
    if not invitation or invitation.orgId != org_id:
        raise HTTPException(status_code=404, detail="Invitation not found")

    if body.status == InvitationStatus.ACCEPTED:
        invitation_repo.accept(invitation)
    elif body.status == InvitationStatus.CANCELLED:
        invitation_repo.cancel(invitation)
    elif body.status == InvitationStatus.EXPIRED:
        invitation_repo.expire(invitation)
    else:
        raise HTTPException(status_code=400, detail="Invalid status transition")

    db.commit()
    return DataResponse(data=invitation)


@org_invitation_router.delete("/{org_id}/invitations/{invitation_id}", response_model=MessageResponse)
def delete_invitation(
    org_id: str,
    invitation_id: str,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    invitation_repo = InvitationRepository(db)
    invitation = invitation_repo.get_by_id(invitation_id)
    if not invitation or invitation.orgId != org_id:
        raise HTTPException(status_code=404, detail="Invitation not found")

    invitation_repo.soft_delete(invitation)
    db.commit()
    return MessageResponse(message="Invitation deleted successfully")