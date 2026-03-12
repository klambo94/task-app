from starlette import status
from starlette.status import HTTP_404_NOT_FOUND

from settings import FRONT_END_URL
from fastapi import FastAPI, HTTPException

from routers import auth, orgs, spaces, sprint, labels, status, comments, threads, users
from fastapi.middleware.cors import CORSMiddleware


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
    raise HTTPException(status_code=HTTP_404_NOT_FOUND)

psinaptic.include_router(auth.router)
psinaptic.include_router(users.router)
psinaptic.include_router(orgs.router)
psinaptic.include_router(spaces.router)
psinaptic.include_router(sprint.router)
psinaptic.include_router(threads.router)
psinaptic.include_router(status.router)
psinaptic.include_router(labels.router)
psinaptic.include_router(comments.router)
