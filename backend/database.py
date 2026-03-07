import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase


POSTGRES_USER : str = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_SERVER : str = os.getenv("POSTGRES_SERVER","localhost")
POSTGRES_PORT : str = os.getenv("POSTGRES_PORT",5432) # default postgres port is 5432
POSTGRES_DB : str = os.getenv("POSTGRES_DB","task-app")

print(f"USER: {POSTGRES_USER}")
print(f"PASSWORD: {POSTGRES_PASSWORD}")
print(f"SERVER: {POSTGRES_SERVER}")
print(f"DB: {POSTGRES_DB}")

DATABASE_URL = f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"
engine = create_engine(url=DATABASE_URL)
SessionLocal = sessionmaker(autocommit= False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass