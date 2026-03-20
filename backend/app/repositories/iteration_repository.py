from datetime import datetime, timezone
from sqlalchemy.orm import Session

from app.lib import CursorPage, paginate, generate_id
from app.models.iteration_model import Iteration
from app.models.enums import IterationType


class IterationRepository:

    def __init__(self, db: Session):
        self.db = db

    # ------------------------------------------------------------------
    # Reads
    # ------------------------------------------------------------------

    def get_by_id(self, iteration_id: str) -> Iteration | None:
        return (
            self.db.query(Iteration)
            .filter(Iteration.id == iteration_id, Iteration.deletedAt.is_(None))
            .first()
        )

    def list_by_space(
            self,
            space_id: str,
            type: IterationType | None = None,
            cursor: str | None = None,
            limit: int = 20,
    ) -> CursorPage:
        """
        List iterations for a space. Optionally filter by type so callers
        can fetch only sprints, only releases, etc.
        """
        query = (
            self.db.query(Iteration)
            .filter(Iteration.spaceId == space_id, Iteration.deletedAt.is_(None))
        )
        if type is not None:
            query = query.filter(Iteration.type == type)

        query = query.order_by(Iteration.createdAt.desc(), Iteration.id.desc())
        return paginate(query, cursor, limit)

    # ------------------------------------------------------------------
    # Writes
    # ------------------------------------------------------------------

    def create(
            self,
            space_id: str,
            status_id: str,
            title: str,
            type: IterationType = IterationType.SPRINT,
            description: str | None = None,
            goal: str | None = None,
            start_date: datetime | None = None,
            end_date: datetime | None = None,
    ) -> Iteration:
        iteration = Iteration(
            id=generate_id(),
            spaceId=space_id,
            statusId=status_id,
            type=type,
            title=title,
            description=description,
            goal=goal,
            startDate=start_date,
            endDate=end_date,
        )
        self.db.add(iteration)
        self.db.flush()
        return iteration

    def update(
            self,
            iteration: Iteration,
            type: IterationType | None = None,
            status_id: str | None = None,
            title: str | None = None,
            description: str | None = None,
            goal: str | None = None,
            start_date: datetime | None = None,
            end_date: datetime | None = None,
    ) -> Iteration:
        if type is not None:
            iteration.type = type
        if status_id is not None:
            iteration.statusId = status_id
        if title is not None:
            iteration.title = title
        if description is not None:
            iteration.description = description
        if goal is not None:
            iteration.goal = goal
        if start_date is not None:
            iteration.startDate = start_date
        if end_date is not None:
            iteration.endDate = end_date
        self.db.flush()
        return iteration

    def soft_delete(self, iteration: Iteration) -> Iteration:
        iteration.deletedAt = datetime.now(timezone.utc)
        self.db.flush()
        return iteration