from datetime import datetime, timezone
from sqlalchemy.orm import Session

from app.lib import paginate, generate_id, CursorPage
from app.models.space_model import Space


class SpaceRepository:

    def __init__(self, db: Session):
        self.db = db

    # ------------------------------------------------------------------
    # Reads
    # ------------------------------------------------------------------

    def get_by_id(self, space_id: str) -> Space | None:
        return (
            self.db.query(Space)
            .filter(Space.id == space_id, Space.deletedAt.is_(None))
            .first()
        )

    def get_by_slug(self, org_id: str, slug: str) -> Space | None:
        """Slug is only unique within an org so both fields are required."""
        return (
            self.db.query(Space)
            .filter(
                Space.orgId == org_id,
                Space.slug == slug,
                Space.deletedAt.is_(None),
            )
            .first()
        )

    def list_by_org(self, org_id: str, cursor: str | None = None, limit: int = 20) -> CursorPage:
        query = (
            self.db.query(Space)
            .filter(Space.orgId == org_id, Space.deletedAt.is_(None))
            .order_by(Space.createdAt.desc(), Space.id.desc())
        )
        return paginate(query, cursor, limit)

    # ------------------------------------------------------------------
    # Writes
    # ------------------------------------------------------------------

    def create(self, org_id: str, name: str, slug: str) -> Space:
        space = Space(
            id=generate_id(),
            orgId=org_id,
            name=name,
            slug=slug,
        )
        self.db.add(space)
        self.db.flush()
        return space

    def update(self, space: Space, name: str | None = None, slug: str | None = None) -> Space:
        if name is not None:
            space.name = name
        if slug is not None:
            space.slug = slug
        self.db.flush()
        return space

    def soft_delete(self, space: Space) -> Space:
        space.deletedAt = datetime.now(timezone.utc)
        self.db.flush()
        return space
