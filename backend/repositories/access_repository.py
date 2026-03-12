import logging
from sqlalchemy.orm import Session

from models.organization_model import OrganizationMember, OrgRole
from models.space_model import Space
from models.sprint_model import Sprint
from models.thread_model import Thread

log = logging.getLogger(__name__)


# Org access ────────────────────────────────────────────────────────────────

def get_org_role(user_id: str, org_id: str, session: Session) -> OrgRole | None:
    member = session.query(OrganizationMember).filter(
        OrganizationMember.userId == user_id,
        OrganizationMember.organizationId == org_id
    ).first()
    return member.role if member else None


def is_org_member(user_id: str, org_id: str, session: Session) -> bool:
    return get_org_role(user_id, org_id, session) is not None


def is_org_admin(user_id: str, org_id: str, session: Session) -> bool:
    role = get_org_role(user_id, org_id, session)
    return role in (OrgRole.OWNER, OrgRole.ADMIN)


def is_org_owner(user_id: str, org_id: str, session: Session) -> bool:
    return get_org_role(user_id, org_id, session) == OrgRole.OWNER


# Space access ──────────────────────────────────────────────────────────────

def can_access_space(user_id: str, space_id: str, session: Session) -> bool:
    space = session.query(Space).filter(Space.id == space_id).first()
    if not space:
        return False
    return is_org_member(user_id, space.organizationId, session)


def can_admin_space(user_id: str, space_id: str, session: Session) -> bool:
    space = session.query(Space).filter(Space.id == space_id).first()
    if not space:
        return False
    # space owner can always admin their own space
    if space.ownerId == user_id:
        return True
    return is_org_admin(user_id, space.organizationId, session)


# Sprint access ─────────────────────────────────────────────────────────────

def can_access_sprint(user_id: str, sprint_id: str, session: Session) -> bool:
    sprint = session.query(Sprint).filter(Sprint.id == sprint_id).first()
    if not sprint:
        return False
    return can_access_space(user_id, sprint.spaceId, session)


# Thread access ─────────────────────────────────────────────────────────────

def can_access_thread(user_id: str, thread_id: str, session: Session) -> bool:
    thread = session.query(Thread).filter(Thread.id == thread_id).first()
    if not thread:
        return False
    return can_access_space(user_id, thread.spaceId, session)


def can_delete_thread(user_id: str, thread_id: str, session: Session) -> bool:
    thread = session.query(Thread).filter(Thread.id == thread_id).first()
    if not thread:
        return False
    # reporter (creator) can always delete their own thread
    if thread.reporterId == user_id:
        return True
    return can_admin_space(user_id, thread.spaceId, session)