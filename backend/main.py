import os
from datetime import datetime, timezone
from typing import Optional

from sqlalchemy.orm import Session

from database import Base, engine, SessionLocal
from models import Status, Task
from fastapi import FastAPI, Depends, HTTPException

import repository
from repository import fetch_task_by_id
from schemas import TaskResponse, TaskCreate, TaskUpdate
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(engine)
app = FastAPI()

FRONT_END_URL : str = os.getenv("FRONT_END_URL","http://localhost:3000")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000",  # Next.js dev server
    FRONT_END_URL],
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db():
    print("\n--- get_db called ---")

    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

@app.get("/")
async def root():
    return {"message": "Hello Tasks!"}

@app.get("/api/tasks", response_model=list[TaskResponse])
async def get_tasks(status: Optional[Status] = None, session: Session = Depends(get_db)):
    return repository.fetch_all_tasks(session=session, status=status)

@app.get("/api/task/{task_id}", response_model= TaskResponse)
async def get_task(task_id: int, session: Session = Depends(get_db)):

    if task_id is None or 0 <= task_id > repository.count_of_tasks(session=session):
        raise HTTPException(status_code=404, detail="Malformed task id!")
    else:
        return repository.fetch_task_by_id(task_id, session=session)

@app.post("/api/tasks", response_model= TaskResponse, status_code=201)
async def create_task(task: TaskCreate, session: Session = Depends(get_db)):
    if task is None:
        return None
    else:
        return repository.create_task(task, session=session)


@app.patch("/api/task/{task_id}", response_model= TaskResponse)
async def update_task(task_id: int, task_in: TaskUpdate, session: Session = Depends(get_db)):
    print("Updating Task: {}".format(task_in))
    if task_id is None or task_id is None or  0 <= task_id > repository.count_of_tasks(session=session):
        return None
    else:
        task = fetch_task_by_id(task_id=task_id, session=session)
        if not task:
            return None

        for field, value in task_in.model_dump(exclude_unset=True).items():
            setattr(task, field, value)

        task.updated_at = datetime.now(timezone.utc)  # set it here
        session.commit()
        session.refresh(task)
        return task

@app.delete("/api/task/{task_id}")
async def delete_task(task_id: int, session: Session = Depends(get_db)):
    print("Deleting task id: {}".format(task_id))
    task = fetch_task_by_id(task_id=task_id, session=session)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    return repository.delete_task(task_id=task_id, session=session)
