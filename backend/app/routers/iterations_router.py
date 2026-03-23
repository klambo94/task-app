from fastapi import APIRouter, Query, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_current_user
from app.models import User
from app.repositories import SpaceRepository, IterationRepository
from app.schemas import IterationPage, IterationRead, IterationCreate, IterationUpdate
from app.schemas.response_schema import MessageResponse, DataResponse

spaces_iteration_router = APIRouter(prefix="/spaces", tags=["Iterations"])
iterations_router = APIRouter(prefix="/iterations", tags=["Iterations"])


@spaces_iteration_router.get("/{space_id}/iterations", response_model=DataResponse[IterationPage])
def get_spaces_iterations(
        space_id: str,
        cursor: str | None = Query(default=None),
        limit: int = Query(default = 20, ge=1, le = 100),
        db: Session = Depends(get_db),
        _: User = Depends(get_current_user)
):
    space_repo = SpaceRepository(db)
    iteration_repo = IterationRepository(db)

    space = space_repo.get_by_id(space_id)
    if not space:
        raise HTTPException(status_code=404, detail="Space not found")

    iterations = iteration_repo.list_by_space(space_id=space_id, cursor=cursor, limit=limit)
    return DataResponse(data=iterations)

@spaces_iteration_router.post("/{space_id}/iterations", response_model=DataResponse[IterationRead])
def create_iteration(
        space_id: str,
        body: IterationCreate,
        db: Session = Depends(get_db),
        _: User = Depends(get_current_user)
):
    space_repo = SpaceRepository(db)
    iteration_repo = IterationRepository(db)

    space = space_repo.get_by_id(space_id)
    if not space:
        raise HTTPException(status_code=404, detail="Space not found")

    iteration = iteration_repo.create(space_id=space_id, status_id=body.statusId,
                                      title=body.title, iteration_type=body.type,
                                      description=body.description, goal=body.goal,
                                      start_date=body.startDate, end_date=body.endDate)

    db.commit()
    return DataResponse(data=iteration)


@iterations_router.get("/{iteration_id}", response_model=DataResponse[IterationRead])
def get_iteration(
        iteration_id: str,        db: Session = Depends(get_db),
        _: User = Depends(get_current_user)
):
    iteration_repo = IterationRepository(db)

    iteration = iteration_repo.get_by_id(iteration_id)
    if not iteration:
        raise HTTPException(status_code=404, detail="Iteration not found")
    return DataResponse(data=iteration)


@iterations_router.patch("/{iteration_id}", response_model=DataResponse[IterationRead])
def update_iteration(
        iteration_id: str,
        body: IterationUpdate,
        db: Session = Depends(get_db),
        _: User = Depends(get_current_user)
):
    iteration_repo = IterationRepository(db)

    existing_iteration = iteration_repo.get_by_id(iteration_id)
    if not existing_iteration:
        raise HTTPException(status_code=404, detail="Iteration not found")

    iteration = iteration_repo.update(iteration=existing_iteration,
        iteration_type=body.type,
        status_id=body.statusId,
        title=body.title,
        description=body.description,
        goal=body.goal,
        start_date=body.startDate,
        end_date=body.endDate,
    )

    db.commit()
    return DataResponse(data=iteration)

@iterations_router.delete("/{iteration_id}", response_model=MessageResponse)
def delete_iteration(
        iteration_id: str,
        db: Session = Depends(get_db),
        _: User = Depends(get_current_user)
):


    iteration_repo = IterationRepository(db=db)

    iteration = iteration_repo.get_by_id(iteration_id)
    if not iteration:
        raise HTTPException(status_code=404, detail="Iteration not found")

    try:
        iteration_repo.soft_delete(iteration)
    except IntegrityError:
        raise HTTPException(status_code=409, detail="Iteration is in use and cannot be deleted")

    db.commit()
    return MessageResponse(message="Iteration deleted successfully")
