from enums import Status
from repositories.task_repository import fetch_task_by_id, update_task, delete_task, create_task
from schemas.task_schema import TaskCreate, TaskUpdate


def test_create_task(db):
    task_in = TaskCreate(name="Buy milk", description="From the store", status=Status.OPEN)
    task = create_task(session=db, task_in=task_in)

    assert task.id is not None
    assert task.name == "Buy milk"
    assert task.status == Status.OPEN

def test_get_task_not_found(db):
    task = fetch_task_by_id(session=db, task_id=999)
    assert task is None

def test_update_task(db):
    task_in = TaskCreate(name="Buy milk", description="From the store", status=Status.OPEN)
    task = create_task(session=db, task_in=task_in)
    db.commit()
    db.refresh(task)

    task_update = TaskUpdate(id=task.id,
                             name="Buy whole milk and heavy cream",
                             description="From the store",
                             status=Status.OPEN)

    task_in.status = Status.COMPLETED
    updated = update_task(session=db, task_in=task_update)
    assert task_update.name == updated.name
    assert task_update.description == updated.description
    assert task_update.status == updated.status

def test_delete_task(db):
    task_in = TaskCreate(name="Buy milk", description="From the store", status=Status.OPEN)
    task = create_task(session=db, task_in=task_in)

    delete_task(session=db, task_id=task.id)
    assert fetch_task_by_id(session=db, task_id=task.id) is None
