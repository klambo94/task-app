from typing import Optional

from sqlalchemy.orm import Session

from database import Base, engine, SessionLocal
from models import Status, Task
from fastapi import FastAPI, Depends, HTTPException

import repository
from schemas import TaskResponse, TaskCreate, TaskUpdate

Base.metadata.create_all(engine)
app = FastAPI()



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

@app.get("/tasks", response_model=list[TaskResponse])
async def get_tasks(status: Optional[Status] = None, session: Session = Depends(get_db)):
    return repository.fetch_all_tasks(session=session, status=status)

@app.get("/task/{task_id}", response_model= TaskResponse)
async def get_task(task_id: int, session: Session = Depends(get_db)):

    if task_id is None or 0 <= task_id > repository.count_of_tasks(session=session):
        raise HTTPException(status_code=404, detail="Malformed task id!")
    else:
        return repository.fetch_task_by_id(task_id, session=session)

@app.post("/tasks", response_model= TaskResponse, status_code=201)
async def create_task(task: TaskCreate, session: Session = Depends(get_db)):
    if task is None:
        return None
    else:
        return repository.create_task(task, session=session)


@app.patch("/task/update/status/{task_id}", response_model= TaskResponse)
async def update_status(task: TaskUpdate, status: str, session: Session = Depends(get_db)):
    if task is None or task.id is None:
        raise HTTPException(status_code=404, detail="Malformed task id!")

    task.status = Status(status)
    updated = repository.update_task(task_in=task, session=session)

    if not updated:
        raise HTTPException(status_code=404, detail="Task not found!")

    return task

@app.patch("/task/update/{task_id}", response_model= TaskResponse)
async def update_task(task: TaskUpdate, session: Session = Depends(get_db)):
    if task is None or task.id is None or  0 <= task.id > repository.count_of_tasks(session=session):
        raise HTTPException(status_code=404, detail="Malformed task id!")
    else:
        return repository.update_task(task_in=task, session=session)


@app.delete("/task/delete/{task_id}")
async def delete_task(task_id: int, session: Session = Depends(get_db)):
    if task_id is None or 0 <= task_id or task_id > repository.count_of_tasks(session=session):
        raise HTTPException(status_code=404, detail="Malformed task id !")
    else:
        repository.delete_task(task_id=task_id, session=session)
