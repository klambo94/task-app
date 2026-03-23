# app/repositories/status_repository.py

from datetime import datetime, timezone
from sqlalchemy.orm import Session
from app.models.status_model import Status
from app.models.enums import StatusCategory
from app.lib import CursorPage, generate_id, paginate


class StatusRepository:

    def __init__(self, db: Session):
        self.db = db

    # ------------------------------------------------------------------
    # Reads
    # ------------------------------------------------------------------

    def get_by_id(self, status_id: str) -> Status | None:
        return (
            self.db.query(Status)
            .filter(Status.id == status_id, Status.deletedAt.is_(None))
            .first()
        )


    def get_by_name(self, name: str) -> Status | None:
        return (
            self.db.query(Status)
            .filter(Status.name == name, Status.deletedAt.is_(None))
            .first()
        )

    def list_by_space(self, space_id: str, cursor: str | None = None, limit: int = 20) -> CursorPage:
        query = (
            self.db.query(Status)
            .filter(Status.spaceId == space_id, Status.deletedAt.is_(None))
            .order_by(Status.sortOrder.asc(), Status.createdAt.desc(), Status.id.desc())
        )
        return paginate(query, cursor, limit)
    # ------------------------------------------------------------------
    # Writes
    # ------------------------------------------------------------------

    def create(
        self,
        space_id: str,
        name: str,
        color: str = "#6B7280",
        category: StatusCategory = StatusCategory.TODO,
        sort_order: int = 0,
    ) -> Status:
        status = Status(
            id=generate_id(),
            spaceId=space_id,
            name=name,
            color=color,
            category=category,
            sortOrder=sort_order,
        )
        self.db.add(status)
        self.db.flush()
        return status

    def update(
        self,
        status: Status,
        name: str | None = None,
        color: str | None = None,
        category: StatusCategory | None = None,
        sort_order: int | None = None,
    ) -> Status:
        if name is not None:
            status.name = name
        if color is not None:
            status.color = color
        if category is not None:
            status.category = category
        if sort_order is not None:
            status.sortOrder = sort_order
        self.db.flush()
        return status

    def soft_delete(self, status: Status) -> Status:
        status.deletedAt = datetime.now(timezone.utc)
        self.db.flush()
        return status