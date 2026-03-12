import logging
from typing import Optional

from sqlalchemy import Sequence
from sqlalchemy.orm import Session

from models import Thread, ThreadAssignee, ThreadLabel
from schemas import ThreadCreate, ThreadUpdate, ThreadFilter
from utils import generate_id

log = logging.getLogger(__name__)


def create(thread_in: ThreadCreate, session: Session) -> Thread:
    log.debug(f"create_thread: {thread_in.title}")
    thread = Thread(
        id=generate_id(),
        title=thread_in.title,
        description=thread_in.description,
        priority=thread_in.priority,
        spaceId=thread_in.spaceId,
        statusId=thread_in.statusId,
        sprintId=thread_in.sprintId,
        parentId=thread_in.parentId,
        reporterId=thread_in.reporterId,
        reviewerId=thread_in.reviewerId,
        dueDate=thread_in.dueDate,
    )
    session.add(thread)
    session.commit()
    session.refresh(thread)
    return thread


def get_by_id(thread_id: str, session: Session) -> Thread | None:
    return session.query(Thread).filter(Thread.id == thread_id).first()


def get_by_space(space_id: str, filters: ThreadFilter | None, session: Session) -> list[Thread]:
    query = session.query(Thread).filter(Thread.spaceId == space_id)

    if filters:
        if filters.sprintId is not None:
            query = query.filter(Thread.sprintId == filters.sprintId)
        if filters.statusId is not None:
            query = query.filter(Thread.statusId == filters.statusId)
        if filters.priority is not None:
            query = query.filter(Thread.priority == filters.priority)
        if filters.parentId is not None:
            query = query.filter(Thread.parentId == filters.parentId)
        else:
            query = query.filter(Thread.parentId == None)  # top-level only by default
        if filters.assigneeId is not None:
            query = query.join(ThreadAssignee, ThreadAssignee.threadId == Thread.id)\
                         .filter(ThreadAssignee.userId == filters.assigneeId)
        if filters.labelId is not None:
            query = query.join(ThreadLabel, ThreadLabel.threadId == Thread.id)\
                         .filter(ThreadLabel.labelId == filters.labelId)

    return query.all()


def get_by_sprint(sprint_id: str, session: Session) -> Sequence[Thread]:
    return session.query(Thread).filter(Thread.sprintId == sprint_id).all()


def get_subtasks(parent_id: str, session: Session) -> Sequence[Thread]:
    return session.query(Thread).filter(Thread.parentId == parent_id).all()


def update(thread_id: str, thread_in: ThreadUpdate, session: Session) -> Thread | None:
    log.debug(f"update_thread: {thread_id}")
    thread = get_by_id(thread_id, session)

    if not thread:
        log.info(f"Thread not found: {thread_id}")
        return None

    for field, value in thread_in.model_dump(exclude_unset=True).items():
        setattr(thread, field, value)

    session.commit()
    session.refresh(thread)
    return thread


def delete(thread_id: str, session: Session) -> bool:
    log.debug(f"delete_thread: {thread_id}")
    thread = get_by_id(thread_id, session)

    if not thread:
        log.info(f"Thread not found: {thread_id}")
        return False

    session.delete(thread)
    session.commit()
    return True


def assign_user(thread_id: str, user_id: str, session: Session) -> Optional[ThreadAssignee] | ThreadAssignee:
    existing = session.query(ThreadAssignee).filter(
        ThreadAssignee.threadId == thread_id,
        ThreadAssignee.userId == user_id
    ).first()

    if existing:
        return existing

    assignee = ThreadAssignee(threadId=thread_id, userId=user_id)
    session.add(assignee)
    session.commit()
    return assignee


def unassign_user(thread_id: str, user_id: str, session: Session) -> bool:
    assignee = session.query(ThreadAssignee).filter(
        ThreadAssignee.threadId == thread_id,
        ThreadAssignee.userId == user_id
    ).first()

    if not assignee:
        return False

    session.delete(assignee)
    session.commit()
    return True


def add_label(thread_id: str, label_id: str, session: Session) -> Optional[ThreadLabel] | ThreadLabel:
    existing = session.query(ThreadLabel).filter(
        ThreadLabel.threadId == thread_id,
        ThreadLabel.labelId == label_id
    ).first()

    if existing:
        return existing

    thread_label = ThreadLabel(threadId=thread_id, labelId=label_id)
    session.add(thread_label)
    session.commit()
    return thread_label


def remove_label(thread_id: str, label_id: str, session: Session) -> bool:
    thread_label = session.query(ThreadLabel).filter(
        ThreadLabel.threadId == thread_id,
        ThreadLabel.labelId == label_id
    ).first()

    if not thread_label:
        return False

    session.delete(thread_label)
    session.commit()
    return True


def move_to_sprint(thread_id: str, sprint_id: str | None, session: Session) -> Thread | None:
    thread = get_by_id(thread_id, session)

    if not thread:
        return None

    thread.sprintId = sprint_id
    session.commit()
    session.refresh(thread)
    return thread


def move_to_space(thread_id: str, space_id: str, session: Session) -> Thread | None:
    thread = get_by_id(thread_id, session)

    if not thread:
        return None

    thread.spaceId = space_id
    thread.sprintId = None  # clear sprint since it belongs to the old space
    session.commit()
    session.refresh(thread)
    return thread