import logging
from typing import Optional

from sqlalchemy import Sequence
from sqlalchemy.orm import Session

from models import SprintStatus, Sprint
from schemas import SprintCreate, SprintUpdate, SprintStatusCreate, SprintStatusUpdate
from utils import generate_id

log = logging.getLogger(__name__)


# Sprint  -----------------------------------------------------------------------------

def create(sprint_in: SprintCreate, session: Session) -> Sprint:
    log.debug(f"create_sprint: {sprint_in.name}")
    sprint = Sprint(
        id=generate_id(),
        name=sprint_in.name,
        goal=sprint_in.goal if hasattr(sprint_in, 'goal') else None,
        spaceId=sprint_in.spaceId,
        statusId=sprint_in.statusId,
        startDate=sprint_in.startDate,
        endDate=sprint_in.endDate,
    )
    session.add(sprint)
    session.commit()
    session.refresh(sprint)
    return sprint


def get_by_id(sprint_id: str, session: Session) -> Sprint | None:
    return session.query(Sprint).filter(Sprint.id == sprint_id).first()


def get_by_space(space_id: str, session: Session) -> Sequence[Sprint]:
    return session.query(Sprint).filter(Sprint.spaceId == space_id).all()


def get_active(space_id: str, session: Session) -> Sprint | None:
    """Returns the first open sprint for a space."""
    return (
        session.query(Sprint)
        .join(SprintStatus, Sprint.statusId == SprintStatus.id)
        .filter(Sprint.spaceId == space_id, SprintStatus.isClosed == False)
        .first()
    )


def update(sprint_id: str, sprint_in: SprintUpdate, session: Session) -> Sprint | None:
    log.debug(f"update_sprint: {sprint_id}")
    sprint = get_by_id(sprint_id, session)

    if not sprint:
        log.info(f"Sprint not found: {sprint_id}")
        return None

    for field, value in sprint_in.model_dump(exclude_unset=True).items():
        setattr(sprint, field, value)

    session.commit()
    session.refresh(sprint)
    return sprint


def delete(sprint_id: str, session: Session) -> bool:
    log.debug(f"delete_sprint: {sprint_id}")
    sprint = get_by_id(sprint_id, session)

    if not sprint:
        log.info(f"Sprint not found: {sprint_id}")
        return False

    session.delete(sprint)
    session.commit()
    return True


# ── SprintStatus ──────────────────────────────────────────────────────────────

def get_sprint_statuses(space_id: str, session: Session) -> Sequence[SprintStatus]:
    return session.query(SprintStatus).filter(SprintStatus.spaceId == space_id).order_by(SprintStatus.order).all()


def create_sprint_status(status_in: SprintStatusCreate, session: Session) -> SprintStatus:
    status = SprintStatus(
        id=generate_id(),
        name=status_in.name,
        color=status_in.color,
        order=status_in.order,
        isDefault=status_in.isDefault,
        isClosed=status_in.isClosed,
        spaceId=status_in.spaceId,
    )
    session.add(status)
    session.commit()
    session.refresh(status)
    return status


def update_sprint_status(status_id: str, status_in: SprintStatusUpdate, session: Session) -> Optional[SprintStatus] | None:
    status = session.query(SprintStatus).filter(SprintStatus.id == status_id).first()

    if not status:
        return None

    for field, value in status_in.model_dump(exclude_unset=True).items():
        setattr(status, field, value)

    session.commit()
    session.refresh(status)
    return status


def delete_sprint_status(status_id: str, session: Session) -> bool:
    status = session.query(SprintStatus).filter(SprintStatus.id == status_id).first()

    if not status:
        return False

    session.delete(status)
    session.commit()
    return True