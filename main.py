
from database import Base, engine, SessionLocal
from models import Task, Status
from fastapi import FastAPI, Depends

import repository
from schemas import TaskResponse, TaskCreate, TaskUpdate

Base.metadata.create_all(engine)
app = FastAPI()



def get_db():

    session = SessionLocal(bind=engine)

    try:
        yield session
    finally:
        session.close()

@app.get("/")
async def root():
    return {"message": "Hello Tasks!"}

@app.get("/tasks", response_model= list[TaskResponse])
async def tasks(session: SessionLocal = Depends(get_db)):
    return repository.fetch_all_tasks(session=session)
@app.get("/tasks/todo", response_model= list[TaskResponse])
async def get_todo_tasks(session: SessionLocal = Depends(get_db)):
    return repository.fetch_all_tasks(status=Status.TO_DO, session=session)

@app.get("/tasks/completed", response_model= list[TaskResponse])
async def get_completed_tasks(session: SessionLocal = Depends(get_db)):
    return repository.fetch_all_tasks(session=session, status=Status.COMPLETED)

@app.get("/tasks/in-progress", response_model= list[TaskResponse])
async def get_in_progress_tasks(session: SessionLocal = Depends(get_db)):
    return repository.fetch_all_tasks(completed=False, session=session, status=Status.IN_PROGRESS)

@app.get("/task/{task_id}", response_model= TaskResponse)
async def get_task(task_id: int, session: SessionLocal = Depends(get_db)):

    if task_id is None or 0 <= task_id < repository.count_of_tasks(session=session):
        return None
    else:
        return repository.fetch_task_by_id(task_id, session=session)

@app.post("/task/create/{task_id}", response_model= TaskResponse)
async def create_task(task: TaskCreate, session: SessionLocal = Depends(get_db)):
    if task is None:
        return None
    else:
        return repository.create_task(task, session=session)



@app.post("/task/update/{task_id}")
async def update_task(task: TaskUpdate, session: SessionLocal = Depends(get_db)):
    if task is None or task.id is None:
        return {"message": "Unable to search with no id not found!"}
    elif 0 <= task.id < repository.count_of_tasks(session=session):
        return {"message": "Invalid task id"}
    else:
        repository.update_task(task_in=task, session=session)
        return {"message": "task updated!"}


@app.post("/task/update/status/{task_id}")
async def update_status(task: TaskUpdate, status: str, session: SessionLocal = Depends(get_db)):
    if (task is None or task.id is None) and (status is not None):
        return {"message": "Invalid task!"}
    elif 0 <= task.id < repository.count_of_tasks(session=session):
        return {"message": "Invalid task id"}
    else:
        task.set_status(status)
        repository.update_task(task_in=task, session=session)
        return {"message": "task status updated!"}

@app.post("/task/delete/{task_id}")
async def delete_task(task: TaskUpdate, session: SessionLocal = Depends(get_db)):
    if task is None or task.id is None:
        return {"message": "Unable to delete with no id not found!"}
    elif 0 <= task.id < repository.count_of_tasks(session=session):
        return {"message": "Invalid task id"}
    else:
        repository.delete_task(task_in=task, session=session)
        return {"message": "task deleted!"}
