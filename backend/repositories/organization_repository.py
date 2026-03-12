import logging
from typing import Optional

import slugify
from sqlalchemy import Sequence
from sqlalchemy.orm import Session

from enums import OrgRole
from models import Organization, OrganizationMember
from repositories import  user_repository
from schemas import OrganizationCreate, OrganizationUpdate
from utils import generate_id

log = logging.getLogger(__name__)

def create(organization_in: OrganizationCreate, session: Session):
    org = Organization(
        id=generate_id(),
        name=organization_in.name,
        ownerId=organization_in.ownerId,
        slug=slugify.slugify(organization_in.name),
    )
    session.add(org)
    session.flush()  # get org.id before creating member

    owner_member = OrganizationMember(
        id=generate_id(),
        organizationId=org.id,
        userId=organization_in.ownerId,
        role=OrgRole.OWNER,
    )
    session.add(owner_member)
    session.commit()
    session.refresh(org)
    return org

def get_by_id(org_id: str, session: Session):
    org = session.query(Organization).filter(Organization.id == org_id).first()
    if not org:
        return None
    return org

def get_by_user(user_id: str, session: Session):
    return(
        session.query(Organization)
        .join(OrganizationMember, OrganizationMember.organizationId == Organization.id)
        .filter(OrganizationMember.userId == user_id)
        .all()
    )

def update(org_id: str, org_in: OrganizationUpdate, session: Session):
    org = session.query(Organization).filter(Organization.id == org_id).first()

    if not org:
        log.error(f"Organization not created! Org: {org_in}")
        return None

    for field, value in org_in.model_dump(exclude_unset=True).items():
        setattr(org, field, value)

    session.commit()
    session.refresh(org)
    return org


def delete(org_id: str, session: Session):
    log.debug(f"delete_org: {org_id}")
    user = get_by_id(org_id, session)

    if not user:
        return False

    session.delete(user)
    session.commit()
    log.info("Organization deleted!")
    return True

def get_members(org_id: str, session: Session) -> Sequence[OrganizationMember]:
    return session.query(OrganizationMember).filter(
        OrganizationMember.organizationId == org_id
    ).all()


def add_member_to_org(org_id: str, user_id: str, session: Session, role: OrgRole = OrgRole.MEMBER ):
    org = get_by_id(org_id, session)
    if not org:
        return None

    user = user_repository.get_by_id(user_id, session)
    if not user:
        return None

    member = OrganizationMember(
        id=generate_id(),
        organizationId=org_id,
        userId=user_id,
        role=role
    )
    session.add(member)
    session.commit()
    return member

def remove_member(org_id: str, user_id: str, session: Session) -> bool:
    member = session.query(OrganizationMember).filter(
        OrganizationMember.organizationId == org_id,
        OrganizationMember.userId == user_id
    ).first()

    if not member:
        log.error(f"Member {user_id} not found in org {org_id}")
        return False

    session.delete(member)
    session.commit()
    return True


def update_member_role(org_id: str, user_id: str, role: OrgRole, session: Session) -> Optional[OrganizationMember] | None:
    member = session.query(OrganizationMember).filter(
        OrganizationMember.organizationId == org_id,
        OrganizationMember.userId == user_id
    ).first()

    if not member:
        log.error(f"Member {user_id} not found in org {org_id}")
        return None

    member.role = role
    session.commit()
    session.refresh(member)
    return member