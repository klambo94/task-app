import os

from config import FRONT_END_URL
from database import Base, engine, SessionLocal
from fastapi import FastAPI

from routers import auth, boards, tasks
from fastapi.middleware.cors import CORSMiddleware

from models import User, Account, Session, VerificationToken, Board, Task


#Create tables
Base.metadata.create_all(engine)
psinaptic = FastAPI()



psinaptic.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000",  # Next.js dev server
    FRONT_END_URL],
    allow_methods=["*"],
    allow_headers=["*"],
)


@psinaptic.get("/")
async def root():
    return {"message": "Hello Tasks!"}

psinaptic.include_router(auth.router)
psinaptic.include_router(boards.router)
psinaptic.include_router(tasks.router)
