from datetime import datetime
from pydantic import EmailStr, BaseModel


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    created_at: datetime

class UserResponse(BaseModel):
    id: str           # Auth.js uses string UUIDs
    name: str | None
    email: str
    image: str | None
    created_at: datetime
    model_config = {"from_attributes": True}

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"