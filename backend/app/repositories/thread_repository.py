from datetime import datetime, timezone
from sqlalchemy.orm import Session

from app.lib import paginate, CursorPage, generate_id
from app.models import Label
from app.models.thread_model import Thread
from app.models.enums import ThreadPriority
from app.schemas import ThreadUpdate
from app.schemas.thread_filter import ThreadFilter


class ThreadRepository:

    def __init__(self, db: Session):
        self.db = db

    # ------------------------------------------------------------------
    # Reads
    # ------------------------------------------------------------------

    def get_by_id(self, thread_id: str) -> Thread | None:
        return (
            self.db.query(Thread)
            .filter(Thread.id == thread_id, Thread.deletedAt.is_(None))
            .first()
        )

    def list_by_space(
            self,
            space_id: str,
            thread_filter: ThreadFilter | None = None,
            cursor: str | None = None,
            limit: int = 20,
    ) -> CursorPage:
        query = (
            self.db.query(Thread)
            .filter(Thread.spaceId == space_id, Thread.deletedAt.is_(None))
        )

        if thread_filter is not None:
            if thread_filter.status_id is not None:
                query = query.filter(Thread.statusId == thread_filter.status_id)
            if thread_filter.assignee_id is not None:
                query = query.filter(Thread.assigneeId == thread_filter.assignee_id)
            if thread_filter.reporter_id is not None:
                query = query.filter(Thread.reporterId == thread_filter.reporter_id)
            if thread_filter.priority is not None:
                query = query.filter(Thread.priority == thread_filter.priority)
            if thread_filter.iteration_id is not None:
                query = query.filter(Thread.iterationId == thread_filter.iteration_id)

        query = query.order_by(Thread.sortOrder.asc(), Thread.createdAt.desc(), Thread.id.desc())
        return paginate(query, cursor, limit)

    def list_backlog(
        self,
        space_id: str,
        cursor: str | None = None,
        limit: int = 20,
    ) -> CursorPage:
        """Threads with no iteration assigned."""
        query = (
            self.db.query(Thread)
            .filter(
                Thread.spaceId == space_id,
                Thread.iterationId.is_(None),
                Thread.deletedAt.is_(None),
            )
            .order_by(Thread.sortOrder.asc(), Thread.createdAt.desc(), Thread.id.desc())
        )
        return paginate(query, cursor, limit)

    # ------------------------------------------------------------------
    # Writes
    # ------------------------------------------------------------------

    def create(
        self,
        space_id: str,
        status_id: str,
        reporter_id: str,
        title: str,
        body: str | None = None,
        assignee_id: str | None = None,
        iteration_id: str | None = None,
        priority: ThreadPriority = ThreadPriority.NONE,
        due_date: datetime | None = None,
        sort_order: int = 0,
    ) -> Thread:
        thread = Thread(
            id=generate_id(),
            spaceId=space_id,
            statusId=status_id,
            reporterId=reporter_id,
            assigneeId=assignee_id,
            iterationId=iteration_id,
            title=title,
            body=body,
            priority=priority,
            dueDate=due_date,
            sortOrder=sort_order,
        )
        self.db.add(thread)
        self.db.flush()
        return thread

    def update(self, thread: Thread,
               update: ThreadUpdate) -> Thread:
        if update.statusId is not None:
            thread.statusId = update.statusId
        if update.assigneeId is not None:
            thread.assigneeId = update.assigneeId
        if update.iterationId is not None:
            thread.iterationId = update.iterationId
        if update.title is not None:
            thread.title = update.title
        if update.body is not None:
            thread.body = update.body
        if update.priority is not None:
            thread.priority = update.priority
        if update.dueDate is not None:
            thread.dueDate = update.dueDate
        if update.sortOrder is not None:
            thread.sortOrder = update.sortOrder
        self.db.flush()
        return thread

    def unassign(self, thread: Thread) -> Thread:
        """Explicitly clear the assignee without requiring a full update call."""
        thread.assigneeId = None
        self.db.flush()
        return thread

    def move_to_backlog(self, thread: Thread) -> Thread:
        """Remove a thread from its iteration and place it in the backlog."""
        thread.iterationId = None
        self.db.flush()
        return thread

    def soft_delete(self, thread: Thread) -> Thread:
        thread.deletedAt = datetime.now(timezone.utc)
        self.db.flush()
        return thread

    def add_label(self, thread: Thread, label: Label) -> Thread:
        if label not in thread.labels:
            thread.labels.append(label)
            self.db.flush()
        return thread

    def remove_label(self, thread: Thread, label: Label) -> Thread:
        if label in thread.labels:
            thread.labels.remove(label)
            self.db.flush()