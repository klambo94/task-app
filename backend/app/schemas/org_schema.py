from pydantic import BaseModel
from datetime import datetime
from app.lib.pagination import CursorPage


# ------------------------------------------------------------------
# Org
# ------------------------------------------------------------------

class OrgBase(BaseModel):
    name: str
    slug: str


class OrgCreate(OrgBase):
    pass


class OrgUpdate(BaseModel):
    name: str | None = None
    slug: str | None = None


class OrgRead(OrgBase):
    id: str
    createdAt: datetime
    updatedAt: datetime

    model_config = {"from_attributes": True}


OrgPage = CursorPage[OrgRead]


# ------------------------------------------------------------------
# OrgMember
# ------------------------------------------------------------------

class OrgMemberBase(BaseModel):
    orgId: str
    userId: str


class OrgMemberCreate(OrgMemberBase):
    pass


class OrgMemberUpdate(BaseModel):
    pass


class OrgMemberRead(OrgMemberBase):
    id: str


OrgMemberPage = CursorPage[OrgMemberRead]