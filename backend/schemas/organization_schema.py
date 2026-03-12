from pydantic import BaseModel
from datetime import datetime
from typing import Optional

from enums import OrgRole


class OrganizationCreate(BaseModel):
    name: str
    ownerId: str


class OrganizationUpdate(BaseModel):
    name: Optional[str] = None
    ownerId: Optional[str] = None


class OrganizationResponse(BaseModel):
    id: str
    name: str
    ownerId: str
    createdAt: datetime
    updatedAt: datetime

    model_config = {"from_attributes": True}


class OrganizationMemberCreate(BaseModel):
    userId: str
    role: OrgRole = OrgRole.MEMBER
    model_config = {"from_attributes": True}


class OrganizationMemberUpdate(BaseModel):
    role: OrgRole


class OrganizationMemberResponse(BaseModel):
    userId: str
    organizationId: str
    role: OrgRole

    model_config = {"from_attributes": True}