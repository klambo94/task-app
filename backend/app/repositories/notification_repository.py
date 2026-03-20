from datetime import datetime, timezone
from sqlalchemy.orm import Session
from app.models.notification_model import Notification
from app.models.enums import NotificationType
from app.lib import CursorPage, generate_id, paginate


class NotificationRepository:

    def __init__(self, db: Session):
        self.db = db

    # ------------------------------------------------------------------
    # Reads
    # ------------------------------------------------------------------

    def get_by_id(self, notification_id: str) -> Notification | None:
        return (
            self.db.query(Notification)
            .filter(Notification.id == notification_id, Notification.deletedAt.is_(None))
            .first()
        )

    def list_by_user(
            self,
            user_id: str,
            unread_only: bool = False,
            cursor: str | None = None,
            limit: int = 20,
    ) -> CursorPage:
        query = (
            self.db.query(Notification)
            .filter(Notification.userId == user_id, Notification.deletedAt.is_(None))
        )
        if unread_only:
            query = query.filter(Notification.isRead == False)  # noqa: E712

        query = query.order_by(Notification.createdAt.desc(), Notification.id.desc())
        return paginate(query, cursor, limit)

    def count_unread(self, user_id: str) -> int:
        """Used to render the notification badge count in the UI."""
        return (
            self.db.query(Notification)
            .filter(
                Notification.userId == user_id,
                Notification.isRead == False,  # noqa: E712
                Notification.deletedAt.is_(None),
            )
            .count()
        )

    # ------------------------------------------------------------------
    # Writes
    # ------------------------------------------------------------------

    def create(
            self,
            user_id: str,
            type: NotificationType,
            resource_id: str,
            resource_type: str,
    ) -> Notification:
        notification = Notification(
            id=generate_id(),
            userId=user_id,
            type=type,
            resourceId=resource_id,
            resourceType=resource_type,
            isRead=False,
        )
        self.db.add(notification)
        self.db.flush()
        return notification

    def mark_as_read(self, notification: Notification) -> Notification:
        notification.isRead = True
        self.db.flush()
        return notification

    def mark_all_as_read(self, user_id: str) -> None:
        """Mark all unread notifications for a user as read in a single query."""
        (
            self.db.query(Notification)
            .filter(
                Notification.userId == user_id,
                Notification.isRead == False,  # noqa: E712
                Notification.deletedAt.is_(None),
            )
            .update({"isRead": True})
        )
        self.db.flush()

    def soft_delete(self, notification: Notification) -> Notification:
        notification.deletedAt = datetime.now(timezone.utc)
        self.db.flush()
        return notification