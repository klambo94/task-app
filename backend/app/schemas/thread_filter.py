from pydantic import BaseModel
from app.models import ThreadPriority

class ThreadFilter(BaseModel):
    status_id: str | None = None
    assignee_id: str | None = None
    reporter_id: str | None = None
    priority: ThreadPriority | None = None
    iteration_id: str | None = None