
from pydantic import BaseModel, EmailStr
from datetime import datetime
from app.lib.pagination import CursorPage


class UserBase(BaseModel):
    email: EmailStr
    name: str | None
    avatarUrl: str | None


class UserCreate(UserBase):
    kindeId: str


class UserUpdate(BaseModel):
    name: str | None = None
    avatarUrl: str | None = None


class UserRead(UserBase):
    id: str
    kindeId: str
    createdAt: datetime
    updatedAt: datetime

    model_config = {"from_attributes": True}


UserPage = CursorPage[UserRead]