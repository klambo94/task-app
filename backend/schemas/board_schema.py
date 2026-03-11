from pydantic import BaseModel
from datetime import datetime

class BoardCreate(BaseModel):
    name: str
    description: str | None = None

class BoardResponse(BaseModel):
    id: str          # string UUID
    name: str
    description: str | None
    user_id: str     # string UUID
    created_at: datetime
    model_config = {"from_attributes": True}