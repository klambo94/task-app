from database import Base
from sqlalchemy import Column, String, DateTime, ForeignKey, Enum as SAEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from enums import OrgRole


class Organization(Base):
    __tablename__ = "organizations"
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    slug = Column(String, unique=True, nullable=False)  # url-friendly name
    image = Column(String, nullable=True)               # org avatar
    ownerId = Column(String, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    createdAt = Column(DateTime(), server_default=func.now())
    updatedAt = Column(DateTime(), server_default=func.now(), onupdate=func.now())

    members = relationship("OrganizationMember", back_populates="organization", cascade="all, delete-orphan")
    spaces = relationship("Space", back_populates="organization", cascade="all, delete-orphan")
    owner = relationship("User", foreign_keys=[ownerId])

    model_config = {"from_attributes": True}

class OrganizationMember(Base):
    __tablename__ = "organization_members"
    id = Column(String, primary_key=True)
    organizationId = Column(String, ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False)
    userId = Column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    role = Column(SAEnum(OrgRole), default=OrgRole.MEMBER, nullable=False)
    createdAt = Column(DateTime(), server_default=func.now())

    organization = relationship("Organization", back_populates="members")
    user = relationship("User", back_populates="organizations")

    model_config = {"from_attributes": True}