import enum


class StatusCategory(str, enum.Enum):
    NOT_STARTED = "not_started"
    STARTED = "started"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class ThreadPriority(str, enum.Enum):
    NO_PRIORITY = "no_priority"
    URGENT = "urgent"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class SpaceVisibility(str, enum.Enum):
    PERSONAL = "personal"
    SHARED = "shared"

class OrgRole(str, enum.Enum):
    OWNER = "owner"
    ADMIN = "admin"
    MEMBER = "member"
