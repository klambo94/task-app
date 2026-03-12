import logging

from sqlalchemy import Sequence
from sqlalchemy.orm import Session

from models import Space
from models import Status
from models import SprintStatus
from schemas import SpaceCreate, SpaceUpdate
from utils import generate_id
from defaults import DEFAULT_STATUSES, DEFAULT_SPRINT_STATUSES

log = logging.getLogger(__name__)


def create(space_in: SpaceCreate, session: Session) -> Space:
    log.debug(f"create_space: {space_in.name}")
    space = Space(
        id=generate_id(),
        name=space_in.name,
        description=space_in.description,
        ownerId=space_in.ownerId,
        organizationId=space_in.organizationId,
        visibility=space_in.visibility,
    )
    session.add(space)
    session.flush()  # need space.id before seeding statuses

    for s in DEFAULT_STATUSES:
        session.add(Status(id=generate_id(), spaceId=space.id, **s))

    for s in DEFAULT_SPRINT_STATUSES:
        session.add(SprintStatus(id=generate_id(), spaceId=space.id, **s))

    session.commit()
    session.refresh(space)
    return space


def get_by_id(space_id: str, session: Session) -> Space | None:
    return session.query(Space).filter(Space.id == space_id).first()


def get_by_org(org_id: str, session: Session) -> Sequence[Space]:
    return session.query(Space).filter(Space.organizationId == org_id).all()


def get_by_user(user_id: str, session: Session) -> Sequence[Space]:
    return session.query(Space).filter(Space.ownerId == user_id).all()


def update(space_id: str, space_in: SpaceUpdate, session: Session) -> Space | None:
    log.debug(f"update_space: {space_id}")
    space = get_by_id(space_id, session)

    if not space:
        log.info(f"Space not found: {space_id}")
        return None

    for field, value in space_in.model_dump(exclude_unset=True).items():
        setattr(space, field, value)

    session.commit()
    session.refresh(space)
    return space


def delete(space_id: str, session: Session) -> bool:
    log.debug(f"delete_space: {space_id}")
    space = get_by_id(space_id, session)

    if not space:
        log.info(f"Space not found: {space_id}")
        return False

    session.delete(space)
    session.commit()
    log.info("Space deleted")
    return True