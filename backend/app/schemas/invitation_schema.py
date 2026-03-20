from pydantic import BaseModel, EmailStr
from datetime import datetime
from app.models.enums import InvitationStatus
from app.lib.pagination import CursorPage


class InvitationBase(BaseModel):
    email: EmailStr


class InvitationCreate(InvitationBase):
    orgId: str
    tokenHash: str
    expiresAt: datetime


class InvitationUpdate(BaseModel):
    status: InvitationStatus


class InvitationRead(InvitationBase):
    id: str
    orgId: str
    expiresAt: datetime
    status: InvitationStatus
    createdAt: datetime
    updatedAt: datetime

    model_config = {"from_attributes": True}


InvitationPage = CursorPage[InvitationRead]