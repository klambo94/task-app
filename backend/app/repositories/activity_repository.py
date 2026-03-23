
from sqlalchemy.orm import Session
from app.lib import paginate, CursorPage
from app.models.thread_activity_model import ThreadActivity


class ActivityRepository:

    def __init__(self, db: Session):
        self.db = db

    def list_by_thread(
        self,
        thread_id: str,
        cursor: str | None = None,
        limit: int = 20,
    ) -> CursorPage:
        query = (
            self.db.query(ThreadActivity)
            .filter(ThreadActivity.threadId == thread_id)
            .order_by(ThreadActivity.createdAt.asc(), ThreadActivity.id.asc())
        )
        return paginate(query, cursor, limit)