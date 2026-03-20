from datetime import datetime, timezone
from sqlalchemy.orm import Session

from app.lib import paginate, CursorPage, generate_id
from app.models.org_model import Org
from app.models.org_member_model import OrgMember


class OrgRepository:

    def __init__(self, db: Session):
        self.db = db

    # ------------------------------------------------------------------
    # Reads
    # ------------------------------------------------------------------

    def get_by_id(self, org_id: str) -> Org | None:
        return (
            self.db.query(Org)
            .filter(Org.id == org_id, Org.deletedAt.is_(None))
            .first()
        )

    def get_by_slug(self, slug: str) -> Org | None:
        return (
            self.db.query(Org)
            .filter(Org.slug == slug, Org.deletedAt.is_(None))
            .first()
        )

    def list(self, cursor: str | None = None, limit: int = 20) -> CursorPage:
        query = (
            self.db.query(Org)
            .filter(Org.deletedAt.is_(None))
            .order_by(Org.createdAt.desc(), Org.id.desc())
        )
        return paginate(query, cursor, limit)

    # ------------------------------------------------------------------
    # Writes
    # ------------------------------------------------------------------

    def create(self, name: str, slug: str) -> Org:
        org = Org(
            id=generate_id(),
            name=name,
            slug=slug,
        )
        self.db.add(org)
        self.db.flush()
        return org

    def update(self, org: Org, name: str | None = None, slug: str | None = None) -> Org:
        if name is not None:
            org.name = name
        if slug is not None:
            org.slug = slug
        self.db.flush()
        return org

    def soft_delete(self, org: Org) -> Org:
        org.deletedAt = datetime.now(timezone.utc)
        self.db.flush()
        return org


class OrgMemberRepository:

    def __init__(self, db: Session):
        self.db = db

    # ------------------------------------------------------------------
    # Reads
    # ------------------------------------------------------------------

    def get_by_id(self, member_id: str) -> OrgMember | None:
        return (
            self.db.query(OrgMember)
            .filter(OrgMember.id == member_id, OrgMember.deletedAt.is_(None))
            .first()
        )

    def get_by_org_and_user(self, org_id: str, user_id: str) -> OrgMember | None:
        """Check if a user is already a member of an org."""
        return (
            self.db.query(OrgMember)
            .filter(
                OrgMember.orgId == org_id,
                OrgMember.userId == user_id,
                OrgMember.deletedAt.is_(None),
            )
            .first()
        )

    def list_by_org(self, org_id: str, cursor: str | None = None, limit: int = 20) -> CursorPage:
        query = (
            self.db.query(OrgMember)
            .filter(OrgMember.orgId == org_id, OrgMember.deletedAt.is_(None))
            .order_by(OrgMember.createdAt.desc(), OrgMember.id.desc())
        )
        return paginate(query, cursor, limit)

    def list_by_user(self, user_id: str, cursor: str | None = None, limit: int = 20) -> CursorPage:
        """Get all orgs a user belongs to."""
        query = (
            self.db.query(OrgMember)
            .filter(OrgMember.userId == user_id, OrgMember.deletedAt.is_(None))
            .order_by(OrgMember.createdAt.desc(), OrgMember.id.desc())
        )
        return paginate(query, cursor, limit)

    # ------------------------------------------------------------------
    # Writes
    # ------------------------------------------------------------------

    def create(self, org_id: str, user_id: str) -> OrgMember:
        member = OrgMember(
            id=generate_id(),
            orgId=org_id,
            userId=user_id,
        )
        self.db.add(member)
        self.db.flush()
        return member

    def soft_delete(self, member: OrgMember) -> OrgMember:
        member.deletedAt = datetime.now(timezone.utc)
        self.db.flush()
        return member
