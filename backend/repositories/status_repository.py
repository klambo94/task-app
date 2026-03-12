import logging

from sqlalchemy import Sequence
from sqlalchemy.orm import Session

from models import Status
from schemas.status_schema import StatusCreate, StatusUpdate, StatusReorder
from utils import generate_id

log = logging.getLogger(__name__)


def create(status_in: StatusCreate, session: Session) -> Status:
    log.debug(f"create_status: {status_in.name}")
    status = Status(
        id=generate_id(),
        name=status_in.name,
        spaceId=status_in.spaceId,
        category=status_in.category,
        color=status_in.color,
        icon=status_in.icon,
        order=status_in.order,
        isDefault=status_in.isDefault,
        isClosed=status_in.isClosed,
    )
    session.add(status)
    session.commit()
    session.refresh(status)
    return status


def get_by_id(status_id: str, session: Session) -> Status | None:
    return session.query(Status).filter(Status.id == status_id).first()


def get_by_space(space_id: str, session: Session) -> Sequence[Status]:
    return session.query(Status).filter(Status.spaceId == space_id).order_by(Status.order).all()


def get_default(space_id: str, session: Session) -> Status | None:
    return session.query(Status).filter(
        Status.spaceId == space_id,
        Status.isDefault == True
    ).first()


def update(status_id: str, status_in: StatusUpdate, session: Session) -> Status | None:
    log.debug(f"update_status: {status_id}")
    status = get_by_id(status_id, session)

    if not status:
        log.info(f"Status not found: {status_id}")
        return None

    for field, value in status_in.model_dump(exclude_unset=True).items():
        setattr(status, field, value)

    session.commit()
    session.refresh(status)
    return status


def reorder(reorders: list[StatusReorder], session: Session) -> bool:
    """Bulk update order field for a list of statuses."""
    for item in reorders:
        status = get_by_id(item.id, session)
        if status:
            status.order = item.order

    session.commit()
    return True


def delete(status_id: str, session: Session) -> bool:
    log.debug(f"delete_status: {status_id}")
    status = get_by_id(status_id, session)

    if not status:
        log.info(f"Status not found: {status_id}")
        return False

    session.delete(status)
    session.commit()
    return True