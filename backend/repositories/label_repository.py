import logging

from sqlalchemy import Sequence
from sqlalchemy.orm import Session

from models import Label
from schemas.label_schema import LabelCreate, LabelUpdate
from utils import generate_id

log = logging.getLogger(__name__)


def create(label_in: LabelCreate, session: Session) -> Label:
    log.debug(f"create_label: {label_in.name}")
    label = Label(
        id=generate_id(),
        name=label_in.name,
        color=label_in.color,
        spaceId=label_in.spaceId,
    )
    session.add(label)
    session.commit()
    session.refresh(label)
    return label


def get_by_id(label_id: str, session: Session) -> Label | None:
    return session.query(Label).filter(Label.id == label_id).first()


def get_by_space(space_id: str, session: Session) -> Sequence[Label]:
    return session.query(Label).filter(Label.spaceId == space_id).all()


def update(label_id: str, label_in: LabelUpdate, session: Session) -> Label | None:
    log.debug(f"update_label: {label_id}")
    label = get_by_id(label_id, session)

    if not label:
        log.info(f"Label not found: {label_id}")
        return None

    for field, value in label_in.model_dump(exclude_unset=True).items():
        setattr(label, field, value)

    session.commit()
    session.refresh(label)
    return label


def delete(label_id: str, session: Session) -> bool:
    log.debug(f"delete_label: {label_id}")
    label = get_by_id(label_id, session)

    if not label:
        log.info(f"Label not found: {label_id}")
        return False

    session.delete(label)
    session.commit()
    return True