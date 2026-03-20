from datetime import datetime, timezone
from sqlalchemy.orm import Session

from app.lib import paginate, CursorPage, generate_id
from app.models.thread_model import Thread
from app.models.enums import ThreadPriority


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
        status_id: str | None = None,
        assignee_id: str | None = None,
        reporter_id: str | None = None,
        priority: ThreadPriority | None = None,
        iteration_id: str | None = None,
        cursor: str | None = None,
        limit: int = 20,
    ) -> CursorPage:
        """
        List threads for a space with optional filters. Supports filtering
        by status, assignee, reporter, priority, and iteration so a single
        endpoint can serve both the board view and the backlog view.
        """
        query = (
            self.db.query(Thread)
            .filter(Thread.spaceId == space_id, Thread.deletedAt.is_(None))
        )

        if status_id is not None:
            query = query.filter(Thread.statusId == status_id)
        if assignee_id is not None:
            query = query.filter(Thread.assigneeId == assignee_id)
        if reporter_id is not None:
            query = query.filter(Thread.reporterId == reporter_id)
        if priority is not None:
            query = query.filter(Thread.priority == priority)
        if iteration_id is not None:
            query = query.filter(Thread.iterationId == iteration_id)

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

    def update(
        self,
        thread: Thread,
        status_id: str | None = None,
        assignee_id: str | None = None,
        iteration_id: str | None = None,
        title: str | None = None,
        body: str | None = None,
        priority: ThreadPriority | None = None,
        due_date: datetime | None = None,
        sort_order: int | None = None,
    ) -> Thread:
        if status_id is not None:
            thread.statusId = status_id
        if assignee_id is not None:
            thread.assigneeId = assignee_id
        if iteration_id is not None:
            thread.iterationId = iteration_id
        if title is not None:
            thread.title = title
        if body is not None:
            thread.body = body
        if priority is not None:
            thread.priority = priority
        if due_date is not None:
            thread.dueDate = due_date
        if sort_order is not None:
            thread.sortOrder = sort_order
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