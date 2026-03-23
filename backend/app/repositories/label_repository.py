from datetime import datetime, timezone
from sqlalchemy.orm import Session
from app.models.label_model import Label
from app.models.thread_model import Thread
from app.lib import CursorPage, generate_id, paginate



class LabelRepository:

    def __init__(self, db: Session):
        self.db = db

    # ------------------------------------------------------------------
    # Reads
    # ------------------------------------------------------------------

    def get_by_id(self, label_id: str) -> Label | None:
        return (
            self.db.query(Label)
            .filter(Label.id == label_id,
                     Label.deletedAt.is_(None))
            .first()
        )

    def get_by_name(self, space_id: str, name: str) -> Label | None:
        """Name is only unique within a space so both fields are required."""
        return (
            self.db.query(Label)
            .filter(
                Label.spaceId == space_id,
                Label.name == name,
                Label.deletedAt.is_(None),
            )
            .first()
        )

    def list_by_space(
            self,
            space_id: str,
            cursor: str | None = None,
            limit: int = 20,
    ) -> CursorPage:
        query = (
            self.db.query(Label)
            .filter(Label.spaceId == space_id,
                    Label.deletedAt.is_(None))
            .order_by(Label.createdAt.desc(),
                      Label.id.desc())
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
    ) -> Label:
        label = Label(
            id=generate_id(),
            spaceId=space_id,
            name=name,
            color=color,
        )
        self.db.add(label)
        self.db.flush()
        return label

    def update(
            self,
            label: Label,
            name: str | None = None,
            color: str | None = None,
    ) -> Label:
        if name is not None:
            label.name = name
        if color is not None:
            label.color = color
        self.db.flush()
        return label

    def add_to_thread(self, thread: Thread, label: Label) -> None:
        """Add a label to a thread if it isn't already applied."""
        if label not in thread.labels:
            thread.labels.append(label)
            self.db.flush()

    def remove_from_thread(self, thread: Thread, label: Label) -> None:
        """Remove a label from a thread if it is currently applied."""
        if label in thread.labels:
            thread.labels.remove(label)
            self.db.flush()

    def soft_delete(self, label: Label) -> Label:
        label.deletedAt = datetime.now(timezone.utc)
        self.db.flush()
        return label
