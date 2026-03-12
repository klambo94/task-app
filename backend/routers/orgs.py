from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from repositories import organization_repository, access_repository
from schemas.organization_schema import (
    OrganizationCreate, OrganizationUpdate, OrganizationResponse,
    OrganizationMemberCreate, OrganizationMemberUpdate, OrganizationMemberResponse,
)
from schemas.shared import DataResponse

from enums import OrgRole

router = APIRouter(prefix="/api/orgs", tags=["orgs"])

@router.get("/", response_model=DataResponse[list[OrganizationResponse]])
def get_orgs(
        user_id: str, # Temp, once auth is hooked up use:  current_user = Depends(current_user)
        session: Session = Depends(get_db)):
    orgs = organization_repository.get_by_user(session=session, user_id=user_id)
    if not orgs:
        raise HTTPException(status_code=404, detail="No Organizations found for user.")
    else:
        return DataResponse(data=orgs)


@router.post("/", response_model=DataResponse[OrganizationResponse])
def create_org(
        org_name: str,
        user_id: str,  # Temp, once auth is hooked up use:  current_user = Depends(current_user)
        session: Session = Depends(get_db)
):
    org_in = OrganizationCreate(name=org_name, ownerId=user_id)
    org = organization_repository.create(organization_in=org_in, session=session)
    return DataResponse(data=org)


@router.get("/{org_id}", response_model=DataResponse[OrganizationResponse])
def get_org(org_id: str,
            user_id: str, # Temp, once auth is hooked up use:  current_user = Depends(current_user)
            session: Session = Depends(get_db)):
    if not access_repository.is_org_member(user_id, org_id, session):
        raise HTTPException(status_code=403, detail="Access denied")

    org = organization_repository.get_by_id(org_id, session)
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")
    return DataResponse(data=org)


@router.patch("/{org_id}", response_model=DataResponse[OrganizationResponse])
def update_org(
        org_id: str,
        org_in: OrganizationUpdate,
        user_id: str,  # Temp, once auth is hooked up use:  current_user = Depends(current_user)
        session: Session = Depends(get_db)
):
    if not access_repository.is_org_admin(user_id, org_id, session):
        raise HTTPException(status_code=403, detail="Admin access required")

    org = organization_repository.update(org_id, org_in, session)
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")
    return DataResponse(data=org)


@router.delete("/{org_id}")
def delete_org(org_id: str,
               user_id: str, # Temp, once auth is hooked up use:  current_user = Depends(current_user)
               session: Session = Depends(get_db)):
    if not access_repository.is_org_owner(user_id, org_id, session):
        raise HTTPException(status_code=403, detail="Owner access required")

    success = organization_repository.delete(org_id, session)
    if not success:
        raise HTTPException(status_code=404, detail="Organization not found")
    return {"message": "Organization deleted"}


# Members  -----------------------------------------------------------------------------

@router.get("/{org_id}/members", response_model=DataResponse[list[OrganizationMemberResponse]])
def get_members(org_id: str,
                user_id: str, # Temp, once auth is hooked up use:  current_user = Depends(current_user)
                session: Session = Depends(get_db)):
    if not access_repository.is_org_member(user_id, org_id, session):
        raise HTTPException(status_code=403, detail="Access denied")

    members = organization_repository.get_members(org_id, session)
    return DataResponse(data=members)


@router.post("/{org_id}/members", response_model=DataResponse[OrganizationMemberResponse])
def add_member(
        org_id: str,
        member_in: OrganizationMemberCreate,
        user_id: str,  # Temp, once auth is hooked up use:  current_user = Depends(current_user)
        session: Session = Depends(get_db)
):
    if not access_repository.is_org_admin(user_id, org_id, session):
        raise HTTPException(status_code=403, detail="Admin access required")

    member = organization_repository.add_member_to_org(
        org_id, member_in.userId, role=member_in.role, session=session
    )
    if not member:
        raise HTTPException(status_code=404, detail="User not found")
    return DataResponse(data=member)


@router.patch("/{org_id}/members/{target_user_id}", response_model=DataResponse[OrganizationMemberResponse])
def update_member_role(
        org_id: str,
        target_user_id: str,
        member_in: OrganizationMemberUpdate,
        user_id: str,  # Temp, once auth is hooked up use:  current_user = Depends(current_user)
        session: Session = Depends(get_db)
):
    if not access_repository.is_org_admin(user_id, org_id, session):
        raise HTTPException(status_code=403, detail="Admin access required")

    # prevent stripping owner role unless you are the owner
    if member_in.role != OrgRole.OWNER and not access_repository.is_org_owner(user_id, org_id, session):
        current_role = access_repository.get_org_role(target_user_id, org_id, session)
        if current_role == OrgRole.OWNER:
            raise HTTPException(status_code=403, detail="Cannot change owner role")

    member = organization_repository.update_member_role(org_id, target_user_id, member_in.role, session)
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    return DataResponse(data=member)


@router.delete("/{org_id}/members/{target_user_id}")
def remove_member(
        org_id: str,
        target_user_id: str,
        user_id: str,  # Temp, once auth is hooked up use:  current_user = Depends(current_user)
        session: Session = Depends(get_db)
):
    if not access_repository.is_org_admin(user_id, org_id, session):
        raise HTTPException(status_code=403, detail="Admin access required")

    success = organization_repository.remove_member(org_id, target_user_id, session)
    if not success:
        raise HTTPException(status_code=404, detail="Member not found")
    return {"message": "Member removed"}