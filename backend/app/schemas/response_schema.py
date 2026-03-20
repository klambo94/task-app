from typing import TypeVar, Generic
from pydantic import BaseModel

T = TypeVar("T")


class DataResponse(BaseModel, Generic[T]):
    """Standard success response wrapper for all endpoints."""
    data: T


class MessageResponse(BaseModel):
    """Used for operations that don't return a resource (e.g. delete, mark as read)."""
    message: str