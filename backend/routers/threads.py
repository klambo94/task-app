import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from repositories import thread_repository, access_repository
from schemas.thread_schema import (
    ThreadCreate, ThreadUpdate, ThreadFilter,
    ThreadResponse, ThreadDetailResponse,
)
from schemas.shared import DataResponse, AssignUserRequest, AddLabelRequest, MoveSprintRequest, MoveSpaceRequest
from enums import ThreadPriority

log = logging.getLogger(__name__)
router = APIRouter(prefix="/api", tags=["threads"])

# Threads -----------------------------------------------------------------------------

@router.get("/spaces/{space_id}/threads", response_model=DataResponse[list[ThreadResponse]])
def get_threads(
    space_id: str,
    user_id: str, # Temp, once auth is hooked up use:  current_user = Depends(get_current_user),
    sprint_id: str | None = None,
    status_id: str | None = None,
    priority: ThreadPriority | None = None,
    assignee_id: str | None = None,
    label_id: str | None = None,
    parent_id: str | None = None,
    session: Session = Depends(get_db)
):
    if not access_repository.can_access_space(user_id, space_id, session):
        raise HTTPException(status_code=403, detail="Access denied")

    filters = ThreadFilter(
        sprintId=sprint_id,
        statusId=status_id,
        priority=priority,
        assigneeId=assignee_id,
        labelId=label_id,
        parentId=parent_id,
    )
    threads = thread_repository.get_by_space(space_id, filters, session)
    return DataResponse(data=threads)


@router.post("/threads", response_model=DataResponse[ThreadResponse])
def create_thread(
    thread_in: ThreadCreate,
    user_id: str, # Temp, once auth is hooked up use:  current_user = Depends(get_current_user),
    session: Session = Depends(get_db)
):
    if not access_repository.can_access_space(user_id, thread_in.spaceId, session):
        raise HTTPException(status_code=403, detail="Access denied")

    thread_in = ThreadCreate(
        title=thread_in.title,
        spaceId=thread_in.spaceId,
        statusId=thread_in.statusId,
        description=thread_in.description,
        priority=thread_in.priority,
        sprintId=thread_in.sprintId,
        parentId=thread_in.parentId,
        reporterId=user_id,
        reviewerId=thread_in.reviewerId,
        dueDate=thread_in.dueDate,
    )
    thread = thread_repository.create(thread_in, session)
    return DataResponse(data=thread)


@router.get("/threads/{thread_id}", response_model=DataResponse[ThreadDetailResponse])
def get_thread(thread_id: str,
               user_id: str,# Temp, once auth is hooked up use:  current_user = Depends(get_current_user)
               session: Session = Depends(get_db)):
    if not access_repository.can_access_thread(user_id, thread_id, session):
        raise HTTPException(status_code=403, detail="Access denied")

    thread = thread_repository.get_by_id(thread_id, session)
    if not thread:
        raise HTTPException(status_code=404, detail="Thread not found")
    return DataResponse(data=thread)


@router.get("/threads/{thread_id}/subtasks", response_model=DataResponse[list[ThreadResponse]])
def get_subtasks(thread_id: str,
                 user_id: str, # Temp, once auth is hooked up use:  current_user = Depends(get_current_user)
                 session: Session = Depends(get_db)):
    if not access_repository.can_access_thread(user_id, thread_id, session):
        raise HTTPException(status_code=403, detail="Access denied")

    subtasks = thread_repository.get_subtasks(thread_id, session)
    return DataResponse(data=subtasks)


@router.patch("/threads/{thread_id}", response_model=DataResponse[ThreadResponse])
def update_thread(
    thread_id: str,
    thread_in: ThreadUpdate,
    user_id: str, # Temp, once auth is hooked up use:  current_user = Depends(get_current_user),
    session: Session = Depends(get_db)
):
    if not access_repository.can_access_thread(user_id, thread_id, session):
        raise HTTPException(status_code=403, detail="Access denied")

    thread = thread_repository.update(thread_id, thread_in, session)
    if not thread:
        raise HTTPException(status_code=404, detail="Thread not found")
    return DataResponse(data=thread)


@router.delete("/threads/{thread_id}")
def delete_thread(thread_id: str,
                  user_id: str, # Temp, once auth is hooked up use:  current_user = Depends(get_current_user)
                  session: Session = Depends(get_db)):
    if not access_repository.can_delete_thread(user_id, thread_id, session):
        raise HTTPException(status_code=403, detail="Access denied")

    success = thread_repository.delete(thread_id, session)
    if not success:
        raise HTTPException(status_code=404, detail="Thread not found")
    return {"message": "Thread deleted"}


# Assignees  -----------------------------------------------------------------------------

@router.post("/threads/{thread_id}/assign")
def assign_user(
    thread_id: str,
    user_id: str, # Temp, once auth is hooked up use:  current_user = Depends(get_current_user),
    payload: AssignUserRequest,
    session: Session = Depends(get_db)
):
    if not access_repository.can_access_thread(user_id, thread_id, session):
        raise HTTPException(status_code=403, detail="Access denied")

    thread_repository.assign_user(thread_id, payload.userId, session)
    return {"message": "User assigned"}


@router.delete("/threads/{thread_id}/assign/{assignee_id}")
def unassign_user(
    thread_id: str,
    assignee_id: str,
    user_id: str, # Temp, once auth is hooked up use:  current_user = Depends(get_current_user),
    session: Session = Depends(get_db)
):
    if not access_repository.can_access_thread(user_id, thread_id, session):
        raise HTTPException(status_code=403, detail="Access denied")

    success = thread_repository.unassign_user(thread_id, assignee_id, session)
    if not success:
        raise HTTPException(status_code=404, detail="Assignee not found")
    return {"message": "User unassigned"}


# Labels  -----------------------------------------------------------------------------

@router.post("/threads/{thread_id}/labels")
def add_label(
    thread_id: str,
    user_id: str, # Temp, once auth is hooked up use:  current_user = Depends(get_current_user),
    payload: AddLabelRequest,
    session: Session = Depends(get_db)
):
    if not access_repository.can_access_thread(user_id, thread_id, session):
        raise HTTPException(status_code=403, detail="Access denied")

    thread_repository.add_label(thread_id, payload.labelId, session)
    return {"message": "Label added"}


@router.delete("/threads/{thread_id}/labels/{label_id}")
def remove_label(
    thread_id: str,
    label_id: str,
    user_id: str, # Temp, once auth is hooked up use:  current_user = Depends(get_current_user),
    session: Session = Depends(get_db)
):
    if not access_repository.can_access_thread(user_id, thread_id, session):
        raise HTTPException(status_code=403, detail="Access denied")

    success = thread_repository.remove_label(thread_id, label_id, session)
    if not success:
        raise HTTPException(status_code=404, detail="Label not found on thread")
    return {"message": "Label removed"}


# Move  -----------------------------------------------------------------------------
@router.patch("/threads/{thread_id}/move-sprint")
def move_to_sprint(
    thread_id: str,
    user_id: str, # Temp, once auth is hooked up use:  current_user = Depends(get_current_user),
    payload: MoveSprintRequest,
    session: Session = Depends(get_db)
):
    if not access_repository.can_access_thread(user_id, thread_id, session):
        raise HTTPException(status_code=403, detail="Access denied")

    thread = thread_repository.move_to_sprint(thread_id, payload.sprintId, session)
    if not thread:
        raise HTTPException(status_code=404, detail="Thread not found")
    return {"message": "Thread moved"}


@router.patch("/threads/{thread_id}/move-space")
def move_to_space(
    thread_id: str,
    user_id: str, # Temp, once auth is hooked up use:  current_user = Depends(get_current_user),
    payload: MoveSpaceRequest,
    session: Session = Depends(get_db)
):
    if not access_repository.can_access_thread(user_id, thread_id, session):
        raise HTTPException(status_code=403, detail="Access denied")

    if not access_repository.can_access_space(user_id, payload.spaceId, session):
        raise HTTPException(status_code=403, detail="Access denied to target space")

    thread = thread_repository.move_to_space(thread_id, payload.spaceId, session)
    if not thread:
        raise HTTPException(status_code=404, detail="Thread not found")
    return {"message": "Thread moved"}