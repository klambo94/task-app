from starlette.testclient import TestClient

from main import psinaptic
from settings import DATABASE_URL
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import settings  # loads .env
from database import Base, get_db
import models  # registers all models



engine = create_engine(DATABASE_URL)
TestingSessionLocal = sessionmaker(bind=engine)


@pytest.fixture(scope="session", autouse=True)
def setup_db():
    """Create all tables once for the test session."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def session():
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture
def client(session, monkeypatch):
    def override_get_db():
        yield session

    psinaptic.dependency_overrides[get_db] = override_get_db
    with TestClient(psinaptic) as c:
        yield c
    psinaptic.dependency_overrides.clear()