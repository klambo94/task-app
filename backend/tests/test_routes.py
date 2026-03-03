from enums import Status
from schemas import TaskCreate




def test_create_task(client):
    task_in = TaskCreate(name="Buy milk", description="From the store", status=Status.OPEN)
    response = client.post("/tasks", json=task_in.model_dump(mode="json"))
    print(response.json())
    assert response.status_code == 201
    assert response.json()["name"] == "Buy milk"

def test_get_task_not_found(client):
    response = client.get("/tasks/999")
    assert response.status_code == 404

def test_list_tasks_filter_by_status(client):
    task1 = TaskCreate(name="Task 1", description="Desc 1", status=Status.OPEN)
    task2 = TaskCreate(name="Task 2", description="Desc 2", status=Status.OPEN)

    client.post("/tasks", json=task1.model_dump(mode="json"))
    client.post("/tasks", json=task2.model_dump(mode="json"))

    response = client.get("/tasks?status=open")
    assert response.status_code == 200
    assert len(response.json()) == 2