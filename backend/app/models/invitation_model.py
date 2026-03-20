from sqlalchemy import Column, String, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship

from app.core.database import Base
from app.models.enums import InvitationStatus
from app.models.mixins.timestamp_mixin import TimestampMixin


class Invitation(TimestampMixin, Base):
    """
    A pending invitation to join an org. The signed token is emailed to the
    invitee; only the hash is stored so raw tokens are never persisted.
    """
    __tablename__ = "invitation"

    id = Column(String, primary_key=True, doc="Internal PK; set via generate_id().")
    orgId = Column(String, ForeignKey("org.id", ondelete="CASCADE"), nullable=False,
                   doc="FK to the org the invitee is being invited to.")
    email = Column(String, nullable=False, doc="Email address the invitation was sent to.")
    tokenHash = Column(
        String, unique=True, nullable=False,
        doc="SHA-256 hash of the signed invitation token. The raw token is only sent via email, never stored.",
    )
    expiresAt = Column(DateTime(timezone=True), nullable=False, doc="UTC expiry time of the invitation token.")
    status = Column(
        Enum(InvitationStatus), nullable=False, default=InvitationStatus.PENDING,
        doc="Lifecycle state of the invitation.",
    )

    org = relationship("Org", back_populates="invitations")

