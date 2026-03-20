import enum


class StatusCategory(str, enum.Enum):
    BACKLOG = "backlog"
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"


class ThreadPriority(str, enum.Enum):
    URGENT = "urgent"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    NONE = "none"


class IterationType(str, enum.Enum):
    SPRINT    = "sprint"
    RELEASE   = "release"
    PHASE     = "phase"
    MILESTONE = "milestone"

class ActivityField(str, enum.Enum):
    STATUS    = "status"
    ASSIGNEE  = "assignee"
    PRIORITY  = "priority"
    DUE_DATE  = "dueDate"
    TITLE     = "title"
    ITERATION = "iteration"  # was SPRINT


class InvitationStatus(str, enum.Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    CANCELLED = "cancelled"
    EXPIRED = "expired"


class NotificationType(str, enum.Enum):
    THREAD_ASSIGNED = "thread_assigned"
    THREAD_COMMENTED = "thread_commented"
    THREAD_MENTIONED = "thread_mentioned"
    SPRINT_STARTED = "sprint_started"
    SPRINT_ENDED = "sprint_ended"
    INVITATION_SENT = "invitation_sent"