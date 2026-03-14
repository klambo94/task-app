import logging
import time

from starlette.status import HTTP_404_NOT_FOUND

from settings import FRONT_END_URL
from fastapi import FastAPI, HTTPException, Request

from routers import orgs, spaces, sprint, labels, status, comments, threads, users
from fastapi.middleware.cors import CORSMiddleware

log = logging.getLogger(__name__)
psinaptic = FastAPI()



psinaptic.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000",  # Next.js dev server
    FRONT_END_URL],
    allow_methods=["*"],
    allow_headers=["*"],
)

# # Logging time taken for each api request
@psinaptic.middleware("http")
async def log_response_time(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    log.info(f"Request: {request.url.path} completed in {process_time:.4f} seconds")
    return response
@psinaptic.get("/")
async def root():
    raise HTTPException(status_code=HTTP_404_NOT_FOUND)

psinaptic.include_router(users.router)
psinaptic.include_router(orgs.router)
psinaptic.include_router(spaces.router)
psinaptic.include_router(sprint.router)
psinaptic.include_router(threads.router)
psinaptic.include_router(status.router)
psinaptic.include_router(labels.router)
psinaptic.include_router(comments.router)
