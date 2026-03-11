from enums import Status
from schemas.task_schema import TaskCreate




def test_create_task(client):
    task_in = TaskCreate(name="Buy milk", description="From the store", status=Status.OPEN)
    response = client.post("/task", json=task_in.model_dump(mode="json"))
    print(response.json())
    assert response.status_code == 201
    assert response.json()["name"] == "Buy milk"

def test_get_task_not_found(client):
    response = client.get("/task/999")
    assert response.status_code == 404

def test_list_tasks_filter_by_status(client):
    task1 = TaskCreate(name="Task 1", description="Desc 1", status=Status.OPEN)
    task2 = TaskCreate(name="Task 2", description="Desc 2", status=Status.OPEN)

    client.post("/task", json=task1.model_dump(mode="json"))
    client.post("/task", json=task2.model_dump(mode="json"))

    response = client.get("/task?status=open")
    assert response.status_code == 200
    assert len(response.json()) == 2