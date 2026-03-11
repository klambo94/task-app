from datetime import datetime, timezone
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from enums import Status
from database import get_db
from schemas.task_schema import TaskResponse, TaskUpdate, TaskCreate
from repositories import task_repository
router = APIRouter(prefix="/api/task", tags=["task"])

@router.get("/", response_model=list[TaskResponse])
async def get_tasks(status: Optional[Status] = None, session: Session = Depends(get_db)):
    return task_repository.fetch_all_tasks(session=session, status=status)

@router.get("/{task_id}", response_model= TaskResponse)
async def get_task(task_id: int, session: Session = Depends(get_db)):

    if task_id is None or 0 <= task_id > task_repository.count_of_tasks(session=session):
        raise HTTPException(status_code=404, detail="Malformed task id!")
    else:
        return task_repository.fetch_task_by_id(task_id, session=session)

@router.post("/", response_model= TaskResponse, status_code=201)
async def create_task(task: TaskCreate, session: Session = Depends(get_db)):
    if task is None:
        return None

    return task_repository.create_task(task, session=session)


@router.patch("/{task_id}", response_model= TaskResponse)
async def update_task(task_id: int, task_in: TaskUpdate, session: Session = Depends(get_db)):
    print("Updating Task: {}".format(task_in))
    if task_id is None or task_id is None or  0 <= task_id > task_repository.count_of_tasks(session=session):
        return None
    else:
        task = task_repository.fetch_task_by_id(task_id=task_id, session=session)
        if not task:
            return None

        for field, value in task_in.model_dump(exclude_unset=True).items():
            setattr(task, field, value)

        task.updated_at = datetime.now(timezone.utc)
        session.commit()
        session.refresh(task)
        return task

@router.delete("/{task_id}")
async def delete_task(task_id: int, session: Session = Depends(get_db)):
    print("Deleting task id: {}".format(task_id))
    task = task_repository.fetch_task_by_id(task_id=task_id, session=session)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    return task_repository.delete_task(task_id=task_id, session=session)