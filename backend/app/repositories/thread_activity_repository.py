from sqlalchemy.orm import Session

from app.lib import generate_id
from app.models.thread_activity_model import ThreadActivity
from app.models.enums import ActivityField


class ThreadActivityRepository:

    def __init__(self, db: Session):
        self.db = db

    # ------------------------------------------------------------------
    # Reads
    # ------------------------------------------------------------------

    def list_by_thread(self, thread_id: str) -> list[ThreadActivity]:
        """
        Returns the full activity timeline for a thread in chronological
        order. Not paginated — the full history is always returned since
        activity timelines are typically rendered in full on the thread
        detail view.
        """
        return (
            self.db.query(ThreadActivity)
            .filter(ThreadActivity.threadId == thread_id)
            .order_by(ThreadActivity.createdAt.asc())
            .all()
        )

    # ------------------------------------------------------------------
    # Writes
    # ------------------------------------------------------------------

    def create(
            self,
            thread_id: str,
            actor_id: str,
            field: ActivityField,
            old_value: str | None,
            new_value: str | None,
    ) -> ThreadActivity:
        activity = ThreadActivity(
            id=generate_id(),
            threadId=thread_id,
            actorId=actor_id,
            field=field,
            oldValue=old_value,
            newValue=new_value,
        )
        self.db.add(activity)
        self.db.flush()
        return activity