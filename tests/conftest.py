import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base
from models import Task
from main import app, get_db

TEST_DATABASE_URL = "sqlite:///:memory:"
TEST_ENGINE = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestSessionLocal = sessionmaker(bind=TEST_ENGINE)
Base.metadata.create_all(bind=TEST_ENGINE)

@pytest.fixture(scope="function")
def db():
    print("\n--- db fixture ---")
    connection = TEST_ENGINE.connect()
    transaction = connection.begin()
    session = TestSessionLocal(bind=connection)
    try:
        yield session
    finally:
        session.close()
        transaction.rollback()  # rolls back all changes, table stays intact
        connection.close()

@pytest.fixture(scope="function")
def client(db):
    def override_get_db():
        print("\n--- override_get_db called ---")
        print("session bind:", db.bind)
        yield db

    app.dependency_overrides[get_db] = override_get_db
    print("\n--- dependency override set ---")
    print("overrides:", app.dependency_overrides)
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()