from sqlalchemy import UniqueConstraint, Column, String, ForeignKey
from sqlalchemy.orm import relationship

from app.core.database import Base
from app.models.mixins.timestamp_mixin import TimestampMixin


class OrgMember(TimestampMixin, Base):
    """
    Junction between User and Org. Carries the member's role within the org.
    """
    __tablename__ = "org_member"
    __table_args__ = (UniqueConstraint("orgId", "userId", name="uq_org_member"),)

    id = Column(String, primary_key=True, doc="Internal PK; set via generate_id().")
    orgId = Column(String, ForeignKey("org.id", ondelete="CASCADE"), nullable=False, doc="FK to the org.")
    userId = Column(String, ForeignKey("user.id", ondelete="CASCADE"), nullable=False, doc="FK to the user.")

    org = relationship("Org", back_populates="members")
    user = relationship("User", back_populates="orgMemberships")
