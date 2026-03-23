from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_current_user
from app.models import User
from app.repositories import NotificationRepository
from app.schemas import NotificationRead, NotificationPage
from app.schemas.response_schema import DataResponse, MessageResponse

notification_router = APIRouter(prefix="/users/me/notifications", tags=["Notifications"])
single_notification_router = APIRouter(prefix="/notifications", tags=["Notifications"])


@notification_router.get("", response_model=DataResponse[NotificationPage])
def list_notifications(
    unread_only: bool = Query(default=False),
    cursor: str | None = Query(default=None),
    limit: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    notification_repo = NotificationRepository(db)
    return DataResponse(data=notification_repo.list_by_user(
        user_id=current_user.id,
        unread_only=unread_only,
        cursor=cursor,
        limit=limit,
    ))


@notification_router.get("/unread-count", response_model=DataResponse[int])
def get_unread_count(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    notification_repo = NotificationRepository(db)
    return DataResponse(data=notification_repo.count_unread(user_id=current_user.id))


@notification_router.post("/read-all", response_model=MessageResponse)
def mark_all_read(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    notification_repo = NotificationRepository(db)
    notification_repo.mark_all_as_read(user_id=current_user.id)
    db.commit()
    return MessageResponse(message="All notifications marked as read")


@single_notification_router.patch("/{notification_id}", response_model=DataResponse[NotificationRead])
def update_notification(
    notification_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    notification_repo = NotificationRepository(db)
    notification = notification_repo.get_by_id(notification_id)
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    if notification.userId != current_user.id:
        raise HTTPException(status_code=403, detail="Not your notification")

    notification_repo.mark_as_read(notification)
    db.commit()
    return DataResponse(data=notification)