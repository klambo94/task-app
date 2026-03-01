import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base
from main import app, get_db

TEST_DATABASE_URL = "sqlite:///:memory:"

@pytest.fixture(scope="function")
def client():
    engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    SessionLocal = sessionmaker(bind=engine)

    def override_get_db():
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()

    # This is the key — swap out the real DB for the test DB
    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as c:
        yield c

    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=engine)


def test_create_task(client):
    response = client.post("/tasks", json={"name": "Buy milk", "description": "From the store"})
    assert response.status_code == 201
    assert response.json()["name"] == "Buy milk"

def test_get_task_not_found(client):
    response = client.get("/tasks/999")
    assert response.status_code == 404

def test_list_tasks_filter_by_status(client):
    client.post("/tasks", json={"name": "Task 1", "description": "..."})
    client.post("/tasks", json={"name": "Task 2", "description": "..."})

    response = client.get("/tasks?status=open")
    assert response.status_code == 200
    assert len(response.json()) == 2