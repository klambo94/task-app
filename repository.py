from typing import Optional

from fastapi.params import Depends
from sqlalchemy.orm import Session

from models import Task, Status
from database import SessionLocal
from datetime import datetime

import logging

from schemas import TaskCreate, TaskUpdate

log = logging.getLogger(__name__)


def fetch_all_tasks(session: Session = Depends(SessionLocal), status: Optional[Status] = None):
    # Todo: implement batch loading  (load first 10, next 10, etc) functionality later..

    if status is not None:
        log.info("Fetching all tasks by status: {status}".format(status=status))
        tasks = session.query(Task).filter(Task.status.lower() == status.lower()).all()
    else:
        tasks = session.query(Task).all()

    return tasks


def fetch_task_by_id( task_id: int, session: Session = Depends(SessionLocal)):
    log.info(f"Fetching task by id: {task_id}")

    if task_id is None:
        log.info(f"Task was not found: {task_id}")
        return None


    task = session.query(Task).filter(Task.id == task_id).first()
    log.debug(f"Fetched task: {task}")
    return task

def create_task(task_in: TaskCreate, session: Session = Depends(SessionLocal)):
    log.info(f"Creating task: {task_in}")
    task = Task(**task_in.model_dump())

    if not task:
        log.info(f"Task was not created: {task}")
        return None


    log.debug(f"Committing task: {task}")
    session.add(task)
    session.commit()
    session.refresh(task)
    return task

def update_task(task_in: TaskUpdate, session: Session = Depends(SessionLocal)):
    log.info(f"Updating task: {task_in}")
    task = fetch_task_by_id(task_id=task_in.id, session=session)
    if not task:
        log.info(f"Task was not found: {task}")
        return None

    newTask = Task(**task_in.model_dump())

    newTask.id = task.id
    newTask.updated_at = datetime.now(datetime.UTC)

    session.update(newTask)
    session.commit()
    session.refresh(newTask)
    log.info("Task Updated!")
    return newTask

def delete_task(task_id: int, session: Session = Depends(SessionLocal)):
    log.info(f"Deleting task: {task_id}")
    task = fetch_task_by_id(session, task_id)
    if not task:
        return None
    session.delete(task)
    session.commit()
    log.info("Task Deleted!")
    return None

def count_of_tasks( session: Session = Depends(SessionLocal)):
    return session.query(Task).count()



