from fastapi import APIRouter, Query, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_current_user
from app.lib import CursorPage
from app.models import User
from app.repositories import ThreadRepository, SpaceRepository, LabelRepository
from app.repositories.activity_repository import ActivityRepository
from app.schemas import ThreadRead, ThreadPage, ThreadCreate, ThreadUpdate, ThreadActivityRead
from app.schemas.response_schema import DataResponse, MessageResponse
from app.schemas.thread_filter import ThreadFilter

thread_router = APIRouter(prefix="/threads", tags=["Threads"])
spaces_thread_router = APIRouter(prefix="/spaces", tags=["Threads"])

@spaces_thread_router.get("/{space_id}/threads", response_model=DataResponse[ThreadPage])
def get_threads(
        space_id: str,
        filters: ThreadFilter = Depends(),
        cursor: str | None = Query(default=None),
        limit: int = Query(default=20, ge=1, le=100),
        db: Session = Depends(get_db),
        _: User = Depends(get_current_user),

):
    thread_repo = ThreadRepository(db=db)
    space_repo = SpaceRepository(db=db)

    space = space_repo.get_by_id(space_id)
    if not space:
        raise HTTPException(status_code=404, detail="Space not found")

    threads = thread_repo.list_by_space(space_id=space.id, thread_filter=filters, cursor=cursor, limit=limit)
    return DataResponse(data=threads)

@spaces_thread_router.post("/{space_id}/threads", response_model=DataResponse[ThreadRead])
def create_thread(
        space_id: str,
        body: ThreadCreate,
        db: Session = Depends(get_db),
        _:User = Depends(get_current_user),
):
    space_repo = SpaceRepository(db=db)
    thread_repo = ThreadRepository(db=db)

    space = space_repo.get_by_id(space_id)
    if not space:
        raise HTTPException(status_code=404, detail="Space not found")

    thread = thread_repo.create(
        space_id=space.id,
        status_id=body.statusId,
        reporter_id=body.reporterId,
        title=body.title,
        assignee_id=body.assigneeId,
        iteration_id=body.iterationId,
        priority=body.priority,
        due_date=body.dueDate,
        sort_order=body.sortOrder,
    )

    db.commit()
    return DataResponse(data=thread)

@thread_router.get("/{thread_id}", response_model=DataResponse[ThreadRead])
def get_thread(
        thread_id: str,
        db: Session = Depends(get_db),
        _: User = Depends(get_current_user),
):
    thread_repo = ThreadRepository(db=db)
    thread = thread_repo.get_by_id(thread_id)
    if not thread:
        raise HTTPException(status_code=404, detail="Thread not found")
    return DataResponse(data=thread)

@thread_router.patch("/{thread_id}", response_model=DataResponse[ThreadRead])
def update_thread(
        thread_id: str,
        body: ThreadUpdate,
        db: Session = Depends(get_db),
        _: User = Depends(get_current_user),
):
    thread_repo = ThreadRepository(db=db)
    thread = thread_repo.get_by_id(thread_id)
    if not thread:
        raise HTTPException(status_code=404, detail="Thread not found")
    thread = thread_repo.update(thread=thread, update=body)
    db.commit()
    return DataResponse(data=thread)

@thread_router.delete("/{thread_id}", response_model=MessageResponse)
def delete_thread(
        thread_id: str,
        db: Session = Depends(get_db),
        _: User = Depends(get_current_user),
):
    thread_repo = ThreadRepository(db=db)
    thread = thread_repo.get_by_id(thread_id)
    if not thread:
        raise HTTPException(status_code=404, detail="Thread not found")

    thread_repo.soft_delete(thread=thread)
    db.commit()
    return MessageResponse(message="Thread deleted successfully")


@thread_router.post("/{thread_id}/labels/{label_id}", response_model=DataResponse[ThreadRead])
def add_label_to_thread(
        thread_id: str,
        label_id: str,
        db: Session = Depends(get_db),
        _: User = Depends(get_current_user),
):
    thread_repo = ThreadRepository(db)
    label_repo = LabelRepository(db)

    thread = thread_repo.get_by_id(thread_id)
    if not thread:
        raise HTTPException(status_code=404, detail="Thread not found")

    label = label_repo.get_by_id(label_id)
    if not label:
        raise HTTPException(status_code=404, detail="Label not found")

    if label.spaceId != thread.spaceId:
        raise HTTPException(status_code=409, detail="Label does not belong to the same space as the thread")

    thread = thread_repo.add_label(thread, label)
    db.commit()
    return DataResponse(data=thread)


@thread_router.delete("/{thread_id}/labels/{label_id}", response_model=MessageResponse)
def remove_label_from_thread(
        thread_id: str,
        label_id: str,
        db: Session = Depends(get_db),
        _: User = Depends(get_current_user),
):
    thread_repo = ThreadRepository(db)
    label_repo = LabelRepository(db)

    thread = thread_repo.get_by_id(thread_id)
    if not thread:
        raise HTTPException(status_code=404, detail="Thread not found")

    label = label_repo.get_by_id(label_id)
    if not label:
        raise HTTPException(status_code=404, detail="Label not found")

    thread_repo.remove_label(thread, label)
    db.commit()
    return MessageResponse(message="Label removed from thread")


@thread_router.get("/{thread_id}/activities", response_model=DataResponse[CursorPage[ThreadActivityRead]])
def get_thread_activities(
    thread_id: str,
    cursor: str | None = Query(default=None),
    limit: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    thread_repo = ThreadRepository(db)
    activity_repo = ActivityRepository(db)

    thread = thread_repo.get_by_id(thread_id)
    if not thread:
        raise HTTPException(status_code=404, detail="Thread not found")

    return DataResponse(data=activity_repo.list_by_thread(thread_id=thread_id, cursor=cursor, limit=limit))