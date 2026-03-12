from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


class UserBase(BaseModel):
    name: Optional[str] = None
    email: EmailStr
    image: Optional[str] = None


class UserUpdate(BaseModel):
    name: Optional[str] = None
    image: Optional[str] = None


class UserResponse(UserBase):
    id: str
    emailVerified: Optional[datetime] = None
    createdAt: datetime
    updatedAt: datetime

    model_config = {"from_attributes": True}