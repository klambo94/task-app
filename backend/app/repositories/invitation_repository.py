from datetime import datetime, timezone
from sqlalchemy.orm import Session
from app.models.invitation_model import Invitation
from app.models.enums import InvitationStatus
from app.lib import CursorPage, generate_id, paginate


class InvitationRepository:

    def __init__(self, db: Session):
        self.db = db

    # ------------------------------------------------------------------
    # Reads
    # ------------------------------------------------------------------

    def get_by_id(self, invitation_id: str) -> Invitation | None:
        return (
            self.db.query(Invitation)
            .filter(Invitation.id == invitation_id, Invitation.deletedAt.is_(None))
            .first()
        )

    def get_by_token_hash(self, token_hash: str) -> Invitation | None:
        """Used during invitation acceptance to look up the invite by the hashed token."""
        return (
            self.db.query(Invitation)
            .filter(Invitation.tokenHash == token_hash, Invitation.deletedAt.is_(None))
            .first()
        )

    def get_pending_by_email(self, org_id: str, email: str) -> Invitation | None:
        """Check if a pending invitation already exists for this email in the org."""
        return (
            self.db.query(Invitation)
            .filter(
                Invitation.orgId == org_id,
                Invitation.email == email,
                Invitation.status == InvitationStatus.PENDING,
                Invitation.deletedAt.is_(None),
            )
            .first()
        )

    def list_by_org(
            self,
            org_id: str,
            status: InvitationStatus | None = None,
            cursor: str | None = None,
            limit: int = 20,
    ) -> CursorPage:
        query = (
            self.db.query(Invitation)
            .filter(Invitation.orgId == org_id, Invitation.deletedAt.is_(None))
        )
        if status is not None:
            query = query.filter(Invitation.status == status)

        query = query.order_by(Invitation.createdAt.desc(), Invitation.id.desc())
        return paginate(query, cursor, limit)

    # ------------------------------------------------------------------
    # Writes
    # ------------------------------------------------------------------

    def create(
            self,
            org_id: str,
            email: str,
            token_hash: str,
            expires_at: datetime,
    ) -> Invitation:
        invitation = Invitation(
            id=generate_id(),
            orgId=org_id,
            email=email,
            tokenHash=token_hash,
            expiresAt=expires_at,
            status=InvitationStatus.PENDING,
        )
        self.db.add(invitation)
        self.db.flush()
        return invitation

    def accept(self, invitation: Invitation) -> Invitation:
        invitation.status = InvitationStatus.ACCEPTED
        self.db.flush()
        return invitation

    def cancel(self, invitation: Invitation) -> Invitation:
        invitation.status = InvitationStatus.CANCELLED
        self.db.flush()
        return invitation

    def expire(self, invitation: Invitation) -> Invitation:
        """Called by a background job to expire stale invitations."""
        invitation.status = InvitationStatus.EXPIRED
        self.db.flush()
        return invitation

    def expire_stale(self) -> int:
        """
        Bulk expire all pending invitations past their expiry date.
        Returns the number of invitations expired.
        """
        now = datetime.now(timezone.utc)
        count = (
            self.db.query(Invitation)
            .filter(
                Invitation.status == InvitationStatus.PENDING,
                Invitation.expiresAt < now,
                Invitation.deletedAt.is_(None),
            )
            .update({"status": InvitationStatus.EXPIRED})
        )
        self.db.flush()
        return count

    def soft_delete(self, invitation: Invitation) -> Invitation:
        invitation.deletedAt = datetime.now(timezone.utc)
        self.db.flush()
        return invitation
