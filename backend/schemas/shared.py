from pydantic import BaseModel
from typing import TypeVar, Generic

T = TypeVar("T")

class DataResponse(BaseModel, Generic[T]):
    data: T


class AssignUserRequest(BaseModel):
    userId: str


class AddLabelRequest(BaseModel):
    labelId: str


class MoveSprintRequest(BaseModel):
    sprintId: str | None = None  # None = move to backlog


class MoveSpaceRequest(BaseModel):
    spaceId: str
